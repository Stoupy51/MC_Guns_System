""" Shared start/respawn command iteration and map-script tag helpers. """
# Imports
from stewbeet import Mem, write_tag, write_versioned_function


# Functions
def write_shared_command_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		# Usage: shared/run_start_commands {mode:"multiplayer"}
		write_versioned_function("shared/run_start_commands", f"""
$data modify storage {ns}:temp _start_cmd_iter set from storage {ns}:$(mode) game.map.start_commands
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/shared/run_start_commands_iter
""")

		write_versioned_function("shared/run_start_commands_iter", f"""
execute store result score #cx {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[0]
execute store result score #cy {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[1]
execute store result score #cz {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[2]

scoreboard players operation #cx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #cy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #cz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _start_cmd.x int 1 run scoreboard players get #cx {ns}.data
execute store result storage {ns}:temp _start_cmd.y int 1 run scoreboard players get #cy {ns}.data
execute store result storage {ns}:temp _start_cmd.z int 1 run scoreboard players get #cz {ns}.data
data modify storage {ns}:temp _start_cmd.command set from storage {ns}:temp _start_cmd_iter[0].command

function {ns}:v{version}/shared/run_start_command with storage {ns}:temp _start_cmd
data remove storage {ns}:temp _start_cmd_iter[0]
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/shared/run_start_commands_iter
""")

		write_versioned_function("shared/run_start_command", "$execute positioned $(x) $(y) $(z) run $(command)")

		# Run as the respawned player. Usage: {mode:"multiplayer"}
		write_versioned_function("shared/run_respawn_commands", f"""
$data modify storage {ns}:temp _respawn_cmd_iter set from storage {ns}:$(mode) game.map.respawn_commands
execute if data storage {ns}:temp _respawn_cmd_iter[0] at @s run function {ns}:v{version}/shared/run_respawn_commands_iter
""")

		write_versioned_function("shared/run_respawn_commands_iter", f"""
data modify storage {ns}:temp _respawn_cmd.command set from storage {ns}:temp _respawn_cmd_iter[0].command

function {ns}:v{version}/shared/run_respawn_command with storage {ns}:temp _respawn_cmd
data remove storage {ns}:temp _respawn_cmd_iter[0]
execute if data storage {ns}:temp _respawn_cmd_iter[0] at @s run function {ns}:v{version}/shared/run_respawn_commands_iter
""")

		write_versioned_function("shared/run_respawn_command", "$execute at @s run $(command)")

		# Map script tags: start (once on activation), tick (every game_tick), join, leave and respawn (as @s), power (interaction).
		for script in ["start", "tick", "join", "leave", "respawn", "power"]:
			write_tag(f"maps/{script}_script", Mem.ctx.data[ns].function_tags, [])

		write_versioned_function("shared/call_at_base", """
$execute positioned $(x) $(y) $(z) run function $(fn)
""")

		# Usage: {mode:"zombies",script:"start"}. Every map script of the tag runs, and each one checks _base.mode.
		write_versioned_function("shared/maps/call_script_at_base", f"""
$execute store result storage {ns}:temp _base.x int 1 run scoreboard players get #$(mode)_base_x {ns}.data
$execute store result storage {ns}:temp _base.y int 1 run scoreboard players get #$(mode)_base_y {ns}.data
$execute store result storage {ns}:temp _base.z int 1 run scoreboard players get #$(mode)_base_z {ns}.data
$data modify storage {ns}:temp _base.mode set value "$(mode)"
$data modify storage {ns}:temp _base.fn set value "#{ns}:maps/$(script)_script"
function {ns}:v{version}/shared/call_at_base with storage {ns}:temp _base
""")

		# Usage: {mode:"multiplayer"}
		write_versioned_function("shared/load_base_coordinates", f"""
$execute store result score #gm_base_x {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[0]
$execute store result score #gm_base_y {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[1]
$execute store result score #gm_base_z {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[2]
$scoreboard players operation #$(mode)_base_x {ns}.data = #gm_base_x {ns}.data
$scoreboard players operation #$(mode)_base_y {ns}.data = #gm_base_y {ns}.data
$scoreboard players operation #$(mode)_base_z {ns}.data = #gm_base_z {ns}.data
""")

		## Modes run side by side, so each entry point of a mode puts its own base and bounds back first. Usage: {mode:"zombies"}
		write_versioned_function("shared/use_map_frame", f"""
$scoreboard players operation #gm_base_x {ns}.data = #$(mode)_base_x {ns}.data
$scoreboard players operation #gm_base_y {ns}.data = #$(mode)_base_y {ns}.data
$scoreboard players operation #gm_base_z {ns}.data = #$(mode)_base_z {ns}.data
$scoreboard players operation #bound_x1 {ns}.data = #$(mode)_bound_x1 {ns}.data
$scoreboard players operation #bound_y1 {ns}.data = #$(mode)_bound_y1 {ns}.data
$scoreboard players operation #bound_z1 {ns}.data = #$(mode)_bound_z1 {ns}.data
$scoreboard players operation #bound_x2 {ns}.data = #$(mode)_bound_x2 {ns}.data
$scoreboard players operation #bound_y2 {ns}.data = #$(mode)_bound_y2 {ns}.data
$scoreboard players operation #bound_z2 {ns}.data = #$(mode)_bound_z2 {ns}.data
""")
		for entry in ("zombies/game_tick", "zombies/preload_complete", "zombies/stop", "multiplayer/game_tick", "multiplayer/stop", "missions/game_tick", "missions/preload_complete", "missions/stop"):
			mode: str = entry.split("/")[0]
			write_versioned_function(entry, f'function {ns}:v{version}/shared/use_map_frame {{mode:"{mode}"}}', prepend=True)

