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
FX_SCORES: list[str] = ["flash_id", "flash_off", "zoom_fx", "zoom_fx_off", "cross_from", "cross_to", "hurt_fx"]
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

    // Bottom strip: green while the clock is armed, red if it never armed. Its width is the
    // elapsed time, one tenth of the screen per tick, so a stuck clock is obvious at a glance.
    if (texCoord.y < 0.03) {
        float ticks = mgs_elapsed(clock, GameTime);
        fragColor = vec4(clock.a < 0.5 ? 1.0 : 0.0, clock.a < 0.5 ? 0.0 : 1.0, 0.0, 1.0);
        if (texCoord.x > fract(ticks / 10.0)) fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
"""
""" `/posteffect add @s mgs:debug_clock` checks the activation clock without launching a round. """


# Functions
def main() -> None:
	""" Register every post effect and the per-tick hooks that keep the applied ids in sync. """
	ns: str = Mem.ctx.project_id

	register_common(ns)
	Mem.ctx.assets[ns].fragment_shaders["post/debug_clock"] = FragmentShader(DEBUG_FSH)
	timed_effect(ns, "debug_clock", f"{ns}:post/debug_clock", {})

	flash.main()
	zoom.main()
	crosshair.main()
	hurt.main()
	write_lifecycle(ns)


def write_lifecycle(ns: str) -> None:
	""" Declare the mirror scores, hook the per-tick expiries, and provide the defensive reset. """
	version: str = Mem.ctx.project_version

	write_load_file("\n".join(f"scoreboard objectives add {ns}.{score} dummy" for score in FX_SCORES) + "\n")

	# Post effects live in player NBT, so a round that ends badly would leave someone scoped for
	# good. Every game start and stop runs this, and a respawn drops them server-side on its own.
	reset_scores: str = "\n".join(f"scoreboard players reset @s {ns}.{score}" for score in FX_SCORES)
	write_versioned_function("player/fx_reset", f"""
posteffect clear @s
{reset_scores}
""")

	write_versioned_function("player/tick", f"""
# Shader ids that expire on their own: the muzzle flash burst and the zoom fade-out
execute if score @s {ns}.flash_off matches 0.. run function {ns}:v{version}/player/flash_tick
execute if score @s {ns}.zoom_fx matches ..-1 run function {ns}:v{version}/zoom/fx_tick

# Low-health overlay. Outside a game it resolves to no tier, which is also how it comes back off.
execute if score #any_game_active {ns}.data matches 1 run function {ns}:v{version}/player/hurt_tick
execute unless score #any_game_active {ns}.data matches 1 if score @s {ns}.hurt_fx matches 1.. run function {ns}:v{version}/player/hurt_tick
""")

