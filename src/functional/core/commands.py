""" Shared start/respawn command iteration and map-script tag helpers. """
from stewbeet import Mem, write_tag, write_versioned_function


def write_shared_command_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		# Run map start commands, e.g. shared/run_start_commands {mode:"multiplayer"}
		write_versioned_function("shared/run_start_commands", f"""
$data modify storage {ns}:temp _start_cmd_iter set from storage {ns}:$(mode) game.map.start_commands
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/shared/run_start_commands_iter
""")

		write_versioned_function("shared/run_start_commands_iter", f"""
# Read relative position
execute store result score #cx {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[0]
execute store result score #cy {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[1]
execute store result score #cz {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[2]

# Convert to absolute
scoreboard players operation #cx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #cy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #cz {ns}.data += #gm_base_z {ns}.data

# Prepare macro args
execute store result storage {ns}:temp _start_cmd.x int 1 run scoreboard players get #cx {ns}.data
execute store result storage {ns}:temp _start_cmd.y int 1 run scoreboard players get #cy {ns}.data
execute store result storage {ns}:temp _start_cmd.z int 1 run scoreboard players get #cz {ns}.data
data modify storage {ns}:temp _start_cmd.command set from storage {ns}:temp _start_cmd_iter[0].command

# Execute and advance
function {ns}:v{version}/shared/run_start_command with storage {ns}:temp _start_cmd
data remove storage {ns}:temp _start_cmd_iter[0]
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/shared/run_start_commands_iter
""")

		write_versioned_function("shared/run_start_command", "$execute positioned $(x) $(y) $(z) run $(command)")

		# Run map respawn commands as the respawned player, e.g. {mode:"multiplayer"}
		write_versioned_function("shared/run_respawn_commands", f"""
$data modify storage {ns}:temp _respawn_cmd_iter set from storage {ns}:$(mode) game.map.respawn_commands
execute if data storage {ns}:temp _respawn_cmd_iter[0] at @s run function {ns}:v{version}/shared/run_respawn_commands_iter
""")

		write_versioned_function("shared/run_respawn_commands_iter", f"""
# Copy command string
data modify storage {ns}:temp _respawn_cmd.command set from storage {ns}:temp _respawn_cmd_iter[0].command

# Execute as current player and advance
function {ns}:v{version}/shared/run_respawn_command with storage {ns}:temp _respawn_cmd
data remove storage {ns}:temp _respawn_cmd_iter[0]
execute if data storage {ns}:temp _respawn_cmd_iter[0] at @s run function {ns}:v{version}/shared/run_respawn_commands_iter
""")

		write_versioned_function("shared/run_respawn_command", "$execute at @s run $(command)")

		# Generic map script tags every mode registers to. start (once on activation), tick (every game_tick), join/leave/respawn (as @s), power (interaction)
		for script in ["start", "tick", "join", "leave", "respawn", "power"]:
			write_tag(f"maps/{script}_script", Mem.ctx.data[ns].function_tags, [])

		# Execute a function positioned at base coordinates
		write_versioned_function("shared/call_at_base", """
$execute positioned $(x) $(y) $(z) run function $(fn)
""")

		# Call a map script tag at base coordinates, e.g. {script:"start"}
		write_versioned_function("shared/maps/call_script_at_base", f"""
execute store result storage {ns}:temp _base.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _base.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _base.z int 1 run scoreboard players get #gm_base_z {ns}.data
$data modify storage {ns}:temp _base.fn set value "#{ns}:maps/$(script)_script"
function {ns}:v{version}/shared/call_at_base with storage {ns}:temp _base
""")

		# Load map base coordinates into scoreboards, e.g. {mode:"multiplayer"}
		write_versioned_function("shared/load_base_coordinates", f"""
$execute store result score #gm_base_x {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[0]
$execute store result score #gm_base_y {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[1]
$execute store result score #gm_base_z {ns}.data run data get storage {ns}:$(mode) game.map.base_coordinates[2]
""")

