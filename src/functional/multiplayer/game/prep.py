""" The warmup phase and the shooting block that holds during it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.lifecycle import GameLifecycle


# Functions
def write_multiplayer_prep() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Shooting Block During Prep Prepend to right_click: block shooting during prep phase
	write_versioned_function("player/right_click", f"""
# Block shooting during multiplayer prep phase
execute if score @s {ns}.mp.in_game matches 1 if data storage {ns}:multiplayer game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

	# Prep Phase Prep tick: during 10s warmup, detect class changes and apply immediately
	write_versioned_function("multiplayer/prep_tick", f"""
# Check for class changes and apply immediately
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.class = @s {ns}.mp.prev_class unless score @s {ns}.mp.class matches 0 at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	## End prep: unfreeze players, transition to active
	write_versioned_function("multiplayer/end_prep", f"""
{GameLifecycle.end_prep_transition_lines(ns, "multiplayer", "mp")}

# Call map start scripts (state is now active, chunks had time to load)
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"start"}}

# Announce
tellraw @a ["","⚔ ",[{{"text":"","color":"green","bold":true}},{{"text":"GO! GO! GO!"}}]]
""")

