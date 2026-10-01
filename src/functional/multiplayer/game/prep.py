""" The warmup phase and the shooting block that holds during it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.lifecycle import GameLifecycle


# Functions
def write_multiplayer_prep() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# No shooting during prep.
	write_versioned_function("player/right_click", f"""
execute if score @s {ns}.mp.in_game matches 1 if data storage {ns}:multiplayer game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

	# During the 10 s warmup, class changes apply at once.
	write_versioned_function("multiplayer/prep_tick", f"""
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.class = @s {ns}.mp.prev_class unless score @s {ns}.mp.class matches 0 at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	write_versioned_function("multiplayer/end_prep", f"""
{GameLifecycle.end_prep_transition_lines(ns, "multiplayer", "mp")}

# The state is now active and chunks had time to load.
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}

tellraw @a ["","⚔ ",[{{"text":"","color":"green","bold":true}},{{"text":"GO! GO! GO!"}}]]
""")

