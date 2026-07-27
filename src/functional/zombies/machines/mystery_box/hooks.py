""" The game tick, preload and stop hooks. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_mystery_box_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hook into game tick for mystery box animation only (interaction handled by Bookshelf)
	write_versioned_function("zombies/game_tick", f"""
# Mystery box animation tick
function {ns}:v{version}/zombies/mystery_box/tick
""")

	## Hook into game start to setup mystery box positions
	write_versioned_function("zombies/preload_complete", f"""
# Setup mystery box positions
execute if data storage {ns}:zombies game.map.mystery_box.positions[0] run function {ns}:v{version}/zombies/mystery_box/setup_positions
""")

	## Hook into stop to reset mystery box
	write_versioned_function("zombies/stop", f"""
# Remove all pull displays and presence boxes, reset all per-box state
kill @e[tag={ns}.mb_display]
kill @e[tag={ns}.mb_presence]
kill @e[tag={ns}.mb_disabled]
kill @e[tag={ns}.mb_temp]
scoreboard players set #mb_pulls {ns}.data 0
scoreboard players set #mb_move_timer {ns}.data 0
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0
scoreboard players reset @a {ns}.mb.pid
scoreboard players set #mb_pid_counter {ns}.data 0
tag @e remove {ns}.mb_fs_active
tag @e remove {ns}.mb_orig_active
""")

