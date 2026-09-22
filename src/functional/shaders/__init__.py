""" Screen post-processing, hosted entirely on `/posteffect`.

Every effect is a per-player id the datapack applies and removes. The server cannot pass a value to
a shader, so each discrete state gets its own id with its parameters baked into the JSON, and each
chain times itself from the activation edge (see [common.py](common.py)).

Nothing here overrides a core shader any more, so the pack no longer depends on the particle
pipeline, on Fabulous graphics, or on the marker-sentinel contract. Iris shaderpacks compose with
all of it, since post effects run after the level is finished.
"""
# Imports
from beet import FragmentShader
from stewbeet import Mem, write_load_file, write_versioned_function

from . import crosshair, flash, hurt, zoom
from .common import HEADER, register_common, timed_effect

# Constants
FX_SCORES: list[str] = [
	"flash_id", "flash_slot", "flash_off",
	"zoom_fx", "zoom_fx_off",
	"cross_from", "cross_to",
	"hurt_fx", "hurt_from", "hurt_pending", "hurt_fall_until", "hurt_out_until",
]
""" Which post effect each player currently has, mirrored as scores so ids can be taken off again. """

DEBUG_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);
    vec4 clock = texture(ClockSampler, vec2(0.5));

    // Bottom strip (texCoord.y grows upward): red if the clock never armed, green while running, blue once settled.
    // Its width is the elapsed time, one tenth of the screen per tick, so a stuck clock is obvious at a glance.
    if (texCoord.y < 0.03) {
        float ticks = mgs_elapsed(clock, GameTime);
        fragColor = clock.a < 0.25 ? vec4(1.0, 0.0, 0.0, 1.0) : clock.a > 0.75 ? vec4(0.0, 0.0, 1.0, 1.0) : vec4(0.0, 1.0, 0.0, 1.0);
        if (texCoord.x > fract(ticks / 10.0)) fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
"""
""" `/posteffect add @s mgs:debug_clock` checks the activation clock without launching a round. """

DEBUG_DEPTH_FSH: str = HEADER + """
uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Magenta: exactly 1.0, the gun as marked by the integrate_depth override.
// Yellow: closer than a tenth of a block, where a shaderpack that squashes hand depth would put the gun.
// Blue: nothing written (sky). Grey: world distance, white near and black at 64 blocks.
void main() {
    float depth = texelFetch(DepthSampler, ivec2(texCoord * vec2(textureSize(InSampler, 0))), 0).r;
    float blocks = 0.05 / max(depth, 1.0e-6);
    vec3 shade = vec3(1.0 - clamp(blocks / 64.0, 0.0, 1.0));
    fragColor = vec4(depth >= 1.0 ? vec3(1.0, 0.0, 1.0) : depth <= 0.0 ? vec3(0.1, 0.2, 0.6) : blocks < 0.1 ? vec3(1.0, 1.0, 0.0) : shade, 1.0);
}
"""
""" `/posteffect add @s mgs:debug_depth` shows how the gun lands in the depth buffer, with and without a shaderpack. """


# Functions
def main() -> None:
	""" Register every post effect and the per-tick hooks that keep the applied ids in sync. """
	ns: str = Mem.ctx.project_id

	register_common(ns)
	Mem.ctx.assets[ns].fragment_shaders["post/debug_clock"] = FragmentShader(DEBUG_FSH)
	timed_effect(ns, "debug_clock", f"{ns}:post/debug_clock", {})
	Mem.ctx.assets[ns].fragment_shaders["post/debug_depth"] = FragmentShader(DEBUG_DEPTH_FSH)
	timed_effect(ns, "debug_depth", f"{ns}:post/debug_depth", {}, inputs=[{"sampler_name": "Depth", "target": "minecraft:main", "use_depth_buffer": True}])

	flash.main()
	zoom.main()
	crosshair.main()
	hurt.main()
	write_lifecycle(ns)


def write_lifecycle(ns: str) -> None:
	""" Declare the mirror scores, hook the per-tick expiries, and provide the defensive reset. """
	version: str = Mem.ctx.project_version

	objectives: str = "\n".join(f"scoreboard objectives add {ns}.{score} dummy" for score in FX_SCORES)
	write_load_file(f"""
{objectives}
scoreboard objectives add {ns}.fx_deaths deathCount
""")

	# Post effects live in player NBT, so a round that ends badly would leave someone scoped for
	# good. Every game start and stop runs this.
	reset_scores: str = "\n".join(f"scoreboard players reset @s {ns}.{score}" for score in FX_SCORES)
	write_versioned_function("player/fx_reset", f"""
posteffect clear @s
{reset_scores}
""")

	# A real death respawns a fresh server player with an empty effect list, so only the mirror
	# scores need forgetting. The crosshair and hurt watchers re-apply on their next tick.
	write_versioned_function("player/fx_after_death", f"""
{reset_scores}
scoreboard players set @s {ns}.fx_deaths 0
""")

	write_versioned_function("player/tick", f"""
# Mirror scores go stale on a real respawn, since the server drops the effect list with the old player
execute if score @s {ns}.fx_deaths matches 1.. run function {ns}:v{version}/player/fx_after_death

# Shader ids that expire on their own: the muzzle flash burst and the zoom and hurt fade-outs
execute if score @s {ns}.flash_off <= #total_tick {ns}.data run function {ns}:v{version}/player/flash_tick
execute if score @s {ns}.zoom_fx matches ..-1 run function {ns}:v{version}/zoom/fx_tick
execute if score @s {ns}.hurt_out_until <= #total_tick {ns}.data run function {ns}:v{version}/player/hurt_out_clear

# Low-health overlay. Outside a game it resolves to no tier, which is also how it comes back off.
execute if score #any_game_active {ns}.data matches 1 run function {ns}:v{version}/player/hurt_tick
execute unless score #any_game_active {ns}.data matches 1 if score @s {ns}.hurt_fx matches 1.. run function {ns}:v{version}/player/hurt_tick
""")

