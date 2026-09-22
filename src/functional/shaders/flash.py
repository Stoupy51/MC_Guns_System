""" Muzzle flash: a depth-falloff light burst on the scene plus an additive spark sprite.

Variants cover the two axes the shader cannot read for itself, Pack-a-Punch and aim-down-sights,
and each variant exists twice. Re-adding the id a player already has can be missed when the remove
and the add land in the same client frame, so consecutive bursts alternate between two slots and a
new burst is always a brand new chain with a fresh clock.
"""
# Imports
from dataclasses import dataclass

from beet import FragmentShader, Texture
from stewbeet import JsonDict, Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
FULL_TICKS: float = 1.0
""" How long the burst stays at full strength, matching the old one-tick particle. """

FADE_END_TICKS: float = 1.6
""" When the burst has faded out completely, 80 ms after it started. """

HOLD_TICKS: int = 2
""" Ticks the id stays applied. It must cover FADE_END_TICKS or the tail gets cut off. """

COOLDOWN_TICKS: int = 2
""" At most one burst every two ticks, ten per second, whatever the weapon's fire rate. """

SPARK_SIZE: int = 1536
""" Side of the spark sheet, a 3x3 grid of nine sprites. """


@dataclass(frozen=True)
class FlashVariant:
	""" One flash look, keyed on what the shooter's gun and the observer's aim change. """
	suffix: str
	""" Appended to "flash" to form the effect id, ex: "_pap_zoom". """
	pap: bool
	zoomed: bool
	""" Whether the observer is aiming down sights, which moves the muzzle to the screen centre. """


FLASH_VARIANTS: list[FlashVariant] = [
	FlashVariant(suffix="",          pap=False, zoomed=False),
	FlashVariant(suffix="_zoom",     pap=False, zoomed=True),
	FlashVariant(suffix="_pap",      pap=True,  zoomed=False),
	FlashVariant(suffix="_pap_zoom", pap=True,  zoomed=True),
]

FLASH_IDS: list[str] = [f"flash{variant.suffix}_{slot}" for variant in FLASH_VARIANTS for slot in (0, 1)]
""" Every applied id. `{ns}.flash_id` stores an index into this list plus one, 0 meaning none. """

FLASH_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D DepthSampler;
uniform sampler2D SparkSampler;

layout(std140) uniform FlashConfig {
    vec4 Color;    // rgb tint of the scene light, a = 1 to tint the sprite as Pack-a-Punch
    vec4 Spark;    // xy = sprite centre in screen space, zw = sprite size
    vec2 Timing;   // ticks at full strength, then ticks until fully faded
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0
#define SPRITE_SQRT 3

// The depth buffer is reversed (cleared to 0, compared GREATER), so near is 1 and the sky is 0.
// Un-reverse before the classic perspective linearization, or the sky reads as point blank and the
// burst floods the whole screen.
float LinearizeDepth(float depth) {
    float z = (1.0 - depth) * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    fragColor = texture(InSampler, texCoord);

    float life = 1.0 - smoothstep(Timing.x, Timing.y, mgs_elapsed(clock, GameTime));
    if (life <= 0.0) return;

    // The held item is drawn before post effects, so without this the spark would sit on the gun.
    // mgs:core/integrate_depth writes it at exactly 1.0, a depth no world geometry can reach.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float rawDepth = texelFetch(DepthSampler, ivec2(texCoord * inSize), 0).r;
    if (rawDepth >= 1.0) return;

    float aspectRatio = inSize.x / inSize.y;
    vec2 oneTexel = 1.0 / inSize;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    float depth = LinearizeDepth(rawDepth);
    float dist = length(vec3(screenCoord * CK * depth, depth));
    if (dist < MAXDIST) {
        vec4 blurColor = fragColor
            + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
            + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
            + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
            + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
        blurColor /= 5.0;

        vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color.rgb * life;
        fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                       * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
        fragColor.rgb += INTENSITY * lightColor * 0.1;
    }

    // The sprite is picked from the activation stamp, so it stays the same sprite for the whole
    // burst instead of resampling scene entropy every frame.
    vec2 lb = Spark.xy - Spark.zw / 2.0;
    vec2 ub = Spark.xy + Spark.zw / 2.0;
    if (screenCoord.x > lb.x && screenCoord.y > lb.y && screenCoord.x < ub.x && screenCoord.y < ub.y) {
        float noise = fract(sin(mgs_unpack_time(clock.rgb) * 1237.0) * 43758.5453);
        int spriteIndex = int(floor(noise * 9.0));
        vec2 spriteOffset = vec2(spriteIndex % SPRITE_SQRT, spriteIndex / SPRITE_SQRT) / float(SPRITE_SQRT);
        vec4 sparkColor = texture(SparkSampler, (screenCoord - lb) / (Spark.zw * float(SPRITE_SQRT)) + spriteOffset);
        if (Color.a > 0.5) {
            sparkColor.rgb *= (noise > 0.5) ? vec3(0.85, 0.1, 1.0) : vec3(1.0, 0.1, 0.45);
        }
        fragColor += sparkColor * life;
    }

    fragColor.a = 1.0;
}
"""

HAND_DEPTH_FSH: str = HEADER + """
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

// Vanilla copies the held item's depth into the main depth buffer here, right before post effects.
// Writing 1.0 instead, the near plane itself, lets a post effect recognise the gun. Nothing else
// reads main depth after this point: it is cleared before the GUI is drawn.
void main() {
    float depth = texelFetch(InSampler, ivec2(gl_FragCoord.xy), 0).r;
    if (depth == 0.0) {
        discard;
    }
    gl_FragDepth = 1.0;
}
"""
""" Override of `minecraft:core/integrate_depth`. If it stops applying, the only loss is the sprite drawing over the gun. """


# Functions
def main() -> None:
	""" Register the flash ids, their shader, the spark sheet, the gun mask and the fire hooks. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/flash"] = FragmentShader(FLASH_FSH)
	Mem.ctx.assets["minecraft"].fragment_shaders["core/integrate_depth"] = FragmentShader(HAND_DEPTH_FSH)

	textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
	Mem.ctx.assets[ns].textures["effect/flash"] = Texture(source_path=f"{textures_folder}/flash.png")

	register_variants(ns)
	write_functions(ns)


def register_variants(ns: str) -> None:
	""" Register both slots of every variant; the two slots of a variant are identical. """
	inputs: list[JsonDict] = [
		{"sampler_name": "Depth", "target": "minecraft:main", "use_depth_buffer": True},
		{"sampler_name": "Spark", "location": f"{ns}:flash", "width": SPARK_SIZE, "height": SPARK_SIZE, "bilinear": True},
	]
	for variant in FLASH_VARIANTS:
		tint: list[float] = [0.6, 0.0, 1.0, 1.0] if variant.pap else [1.0, 0.8, 0.5, 0.0]
		spark: list[float] = [0.0, -0.125, 0.6, 0.6] if variant.zoomed else [0.085, -0.11, 0.45, 0.45]
		for slot in (0, 1):
			timed_effect(
				ns,
				f"flash{variant.suffix}_{slot}",
				f"{ns}:post/flash",
				{"FlashConfig": [
					uniform("Color", "vec4", tint),
					uniform("Spark", "vec4", spark),
					uniform("Timing", "vec2", [FULL_TICKS, FADE_END_TICKS]),
				]},
				inputs=inputs,
			)


def write_functions(ns: str) -> None:
	""" Apply the right id on fire, alternating slots, and take it off once its hold runs out. """
	version: str = Mem.ctx.project_version

	write_versioned_function("player/fire_weapon", f"""
# Shader: muzzle flash for everyone who can see the shooter - skip for grenades
execute store success score #has_pap_level {ns}.data if data storage {ns}:gun all.stats.pap_level
execute if score #has_pap_level {ns}.data matches 1 unless data storage {ns}:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function {ns}:v{version}/player/apply_pap_flash_if_can_see
execute if score #has_pap_level {ns}.data matches 0 unless data storage {ns}:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function {ns}:v{version}/player/apply_flash_if_can_see
""")

	for name, pap in (("apply_flash_if_can_see", False), ("apply_pap_flash_if_can_see", True)):
		adds: list[str] = []
		for variant in (v for v in FLASH_VARIANTS if v.pap == pap):
			aim: str = "if" if variant.zoomed else "unless"
			for slot in (0, 1):
				index: int = FLASH_IDS.index(f"flash{variant.suffix}_{slot}") + 1
				guard: str = f"execute {aim} score @s {ns}.zoom matches 1 if score @s {ns}.flash_slot matches {slot} run"
				adds.append(f"{guard} posteffect add @s {ns}:flash{variant.suffix}_{slot}")
				adds.append(f"{guard} scoreboard players set @s {ns}.flash_id {index}")
		lines: str = "\n".join(adds)
		write_versioned_function(f"player/{name}", f"""
# At most one burst per {COOLDOWN_TICKS} ticks for this observer
execute if score @s {ns}.last_muzzle_flash > #total_tick {ns}.data run return 0
scoreboard players set @s {ns}.last_muzzle_flash {COOLDOWN_TICKS}
scoreboard players operation @s {ns}.last_muzzle_flash += #total_tick {ns}.data

# Check line of sight to the muzzle and set #can_see accordingly (score 0 or 1).
scoreboard players set #can_see {ns}.data 0
execute if entity @s[tag={ns}.ticking] run scoreboard players set #can_see {ns}.data 1
execute if score #can_see {ns}.data matches 0 store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #can_see {ns}.data matches 0 run return 0

# Swap the previous burst for the other slot, so the new one is always a fresh chain.
# The sprite sits at the muzzle, which moves on ADS, so the variant follows this observer's own aim.
function {ns}:v{version}/player/flash_clear
execute store success score #flash_slot_was_1 {ns}.data if score @s {ns}.flash_slot matches 1
execute store result score @s {ns}.flash_slot if score #flash_slot_was_1 {ns}.data matches 0
{lines}

# The flash lights from unmagnified depth, so the zoom must run after it; the crosshair stays on top
function {ns}:v{version}/zoom/fx_to_back
function {ns}:v{version}/zoom/crosshair_to_back
scoreboard players set @s {ns}.flash_off {HOLD_TICKS}
scoreboard players operation @s {ns}.flash_off += #total_tick {ns}.data
""")

	removes: str = "\n".join(
		f"execute if score @s {ns}.flash_id matches {index} run posteffect remove @s {ns}:{effect_id}"
		for index, effect_id in enumerate(FLASH_IDS, start=1)
	)
	write_versioned_function("player/flash_clear", f"""
{removes}
scoreboard players set @s {ns}.flash_id 0
""")

	write_versioned_function("player/flash_tick", f"""
# @s = a player whose burst has been held long enough to have faded out
function {ns}:v{version}/player/flash_clear
scoreboard players reset @s {ns}.flash_off
""")

