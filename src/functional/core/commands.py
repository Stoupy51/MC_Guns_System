""" Shared start/respawn command iteration and map-script tag helpers. """
# Imports
from stewbeet import Mem, write_tag, write_tick_file, write_versioned_function

# Constants
MAP_ENTRIES: dict[str, tuple[str, ...]] = {
	"zombies": ("start", "preload_complete", "end_prep", "game_tick", "freeze_tick", "join_game", "respawn_tp", "stop"),
	"multiplayer": (
		"start", "end_prep", "prep_tick", "game_tick", "join_game", "respawn_tp", "actual_respawn",
		"gamemodes/demo/start_round", "gamemodes/snd/start_round", "stop",
	),
	"missions": ("start", "preload_complete", "end_prep", "prep_tick", "game_tick", "join_game", "respawn_tp", "actual_respawn", "stop"),
}
""" Each mode's functions the server or a player calls from outside its map: they run in the map's dimension, with its base and bounds. """


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
		# The map's own `<script>_command` (start_command, tick_command, set on the base marker) runs after them.
		write_versioned_function("shared/maps/call_script_at_base", f"""
$execute store result storage {ns}:temp _base.x int 1 run scoreboard players get #$(mode)_base_x {ns}.data
$execute store result storage {ns}:temp _base.y int 1 run scoreboard players get #$(mode)_base_y {ns}.data
$execute store result storage {ns}:temp _base.z int 1 run scoreboard players get #$(mode)_base_z {ns}.data
$data modify storage {ns}:temp _base.mode set value "$(mode)"
$data modify storage {ns}:temp _base.fn set value "#{ns}:maps/$(script)_script"
function {ns}:v{version}/shared/call_at_base with storage {ns}:temp _base

$execute unless data storage {ns}:$(mode) game.map.$(script)_command run return 0
$data modify storage {ns}:temp _base.command set from storage {ns}:$(mode) game.map.$(script)_command
function {ns}:v{version}/shared/run_start_command with storage {ns}:temp _base
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

		## Runs an entry point of a mode in the dimension of its selected map, with its base and bounds.
		## #in_<mode>_map stops the nested entries (a stop from a tick) from entering again. Usage: {mode:"zombies",fn:"..."}
		write_versioned_function("shared/enter_map", f"""
$scoreboard players set #in_$(mode)_map {ns}.data 1
$function {ns}:v{version}/shared/use_map_frame {{mode:"$(mode)"}}
$data modify storage {ns}:temp _enter set value {{mode:"$(mode)",fn:"$(fn)",dimension:"minecraft:overworld"}}
$data modify storage {ns}:temp _enter.map_id set from storage {ns}:$(mode) game.map_id
function {ns}:v{version}/shared/enter_map_dimension with storage {ns}:temp _enter
function {ns}:v{version}/shared/enter_map_run with storage {ns}:temp _enter
$scoreboard players set #in_$(mode)_map {ns}.data 0
""")
		write_versioned_function("shared/enter_map_dimension", f"""
$data modify storage {ns}:temp _enter.dimension set from storage {ns}:maps $(mode)[{{id:"$(map_id)"}}].dimension
""")
		write_versioned_function("shared/enter_map_run", "$execute in $(dimension) run function $(fn)")

		# A function that failed halfway must not leave its mode marked as entered.
		write_tick_file("\n".join(f"scoreboard players set #in_{mode}_map {ns}.data 0" for mode in MAP_ENTRIES), prepend=True)
		for mode, entries in MAP_ENTRIES.items():
			for entry in entries:
				write_versioned_function(f"{mode}/{entry}", (
					f"execute unless score #in_{mode}_map {ns}.data matches 1 run return run "
					f'function {ns}:v{version}/shared/enter_map {{mode:"{mode}",fn:"{ns}:v{version}/{mode}/{entry}"}}'
				), prepend=True)

