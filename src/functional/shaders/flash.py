""" Muzzle flash: a depth-falloff light burst on the scene plus an additive spark sprite.

Four ids cover the two axes the shader cannot read for itself, Pack-a-Punch and aim-down-sights.
The datapack knows both at fire time and picks the id, so nothing needs a parameter channel.
"""
# Imports
from beet import FragmentShader, Texture
from stewbeet import JsonDict, Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
DURATION: float = 0.8
""" Visible length in ticks, 40 ms, well under the 1-tick floor the command itself imposes. """

HOLD_TICKS: int = 2
""" Ticks the id stays applied. One tick off between shots is what re-arms the clock. """

SPARK_SIZE: int = 1536
""" Side of the spark sheet, a 3x3 grid of nine sprites. """

FLASH_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D DepthSampler;
uniform sampler2D SparkSampler;

layout(std140) uniform FlashConfig {
    vec4 Color;      // rgb tint of the scene light, a = 1 to tint the sprite as Pack-a-Punch
    vec4 Spark;      // xy = sprite centre in screen space, zw = sprite size
    float Duration;  // ticks
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

    // Decay to nothing well before the id is removed, so the burst is two frames rather than a tick.
    float life = 1.0 - clamp(mgs_elapsed(clock, GameTime) / Duration, 0.0, 1.0);
    if (life <= 0.0) return;

    vec2 inSize = vec2(textureSize(InSampler, 0));
    float aspectRatio = inSize.x / inSize.y;
    vec2 oneTexel = 1.0 / inSize;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    float depth = LinearizeDepth(texture(DepthSampler, texCoord).r);
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


# Functions
def main() -> None:
	""" Register the four flash ids, their shader, the spark sheet, and the fire and expiry hooks. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/flash"] = FragmentShader(FLASH_FSH)

	textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
	Mem.ctx.assets[ns].textures["effect/flash"] = Texture(source_path=f"{textures_folder}/flash.png")

	register_variants(ns)
	write_functions(ns)


def register_variants(ns: str) -> None:
	""" One id per (Pack-a-Punch, zoomed) pair: the sprite sits at the muzzle, which moves on ADS. """
	spark_inputs: list[JsonDict] = [
		{"sampler_name": "Depth", "target": "minecraft:main", "use_depth_buffer": True},
		{"sampler_name": "Spark", "location": f"{ns}:flash", "width": SPARK_SIZE, "height": SPARK_SIZE, "bilinear": True},
	]
	for pap, tint in (("", [1.0, 0.8, 0.5, 0.0]), ("_pap", [0.6, 0.0, 1.0, 1.0])):
		for zoom, spark in (("", [0.085, -0.11, 0.45, 0.45]), ("_zoom", [0.0, -0.125, 0.6, 0.6])):
			timed_effect(
				ns,
				f"flash{pap}{zoom}",
				f"{ns}:post/flash",
				{"FlashConfig": [
					uniform("Color", "vec4", tint),
					uniform("Spark", "vec4", spark),
					uniform("Duration", "float", DURATION),
				]},
				inputs=spark_inputs,
			)


def write_functions(ns: str) -> None:
	""" Apply the right id on fire and take it off again, leaving a tick of gap to re-arm the clock. """
	version: str = Mem.ctx.project_version

	write_versioned_function("player/fire_weapon", f"""
# Shader: muzzle flash for everyone who can see the shooter - skip for grenades
execute store success score #has_pap_level {ns}.data if data storage {ns}:gun all.stats.pap_level
execute if score #has_pap_level {ns}.data matches 1 unless data storage {ns}:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function {ns}:v{version}/player/apply_pap_flash_if_can_see
execute if score #has_pap_level {ns}.data matches 0 unless data storage {ns}:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function {ns}:v{version}/player/apply_flash_if_can_see
""")

	for name, pap, zoomed_slot, hip_slot in (
		("apply_flash_if_can_see",     "",     1, 3),
		("apply_pap_flash_if_can_see", "_pap", 2, 4),
	):
		write_versioned_function(f"player/{name}", f"""
# The clock only re-arms when the id has been absent for a tick, so refuse to re-apply too early
execute if score @s {ns}.last_muzzle_flash > #total_tick {ns}.data run return 0
scoreboard players set @s {ns}.last_muzzle_flash 3
scoreboard players operation @s {ns}.last_muzzle_flash += #total_tick {ns}.data

# Check line of sight to the muzzle and set #can_see accordingly (score 0 or 1).
scoreboard players set #can_see {ns}.data 0
execute if entity @s[tag={ns}.ticking] run scoreboard players set #can_see {ns}.data 1
execute if score #can_see {ns}.data matches 0 store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #can_see {ns}.data matches 0 run return 0

# The sprite sits at the muzzle, which moves on ADS, so the id depends on this observer's own aim
execute if score @s {ns}.zoom matches 1 run posteffect add @s {ns}:flash{pap}_zoom
execute if score @s {ns}.zoom matches 1 run scoreboard players set @s {ns}.flash_id {zoomed_slot}
execute unless score @s {ns}.zoom matches 1 run posteffect add @s {ns}:flash{pap}
execute unless score @s {ns}.zoom matches 1 run scoreboard players set @s {ns}.flash_id {hip_slot}
scoreboard players set @s {ns}.flash_off {HOLD_TICKS}
""")

	write_versioned_function("player/flash_tick", f"""
# @s = a player with a flash applied. Counting down to 0 takes the id off and frees the clock.
scoreboard players remove @s {ns}.flash_off 1
execute if score @s {ns}.flash_off matches 1.. run return 0
execute if score @s {ns}.flash_id matches 1 run posteffect remove @s {ns}:flash_zoom
execute if score @s {ns}.flash_id matches 2 run posteffect remove @s {ns}:flash_pap_zoom
execute if score @s {ns}.flash_id matches 3 run posteffect remove @s {ns}:flash
execute if score @s {ns}.flash_id matches 4 run posteffect remove @s {ns}:flash_pap
scoreboard players set @s {ns}.flash_id 0
scoreboard players reset @s {ns}.flash_off
""")

