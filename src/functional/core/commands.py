
# Shared start/respawn command iteration functions
from stewbeet import Mem, write_versioned_function


def write_shared_command_functions() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run map start commands (relative pos + command string)
	## Usage: function shared/run_start_commands {mode:"multiplayer"}
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

	## Run map respawn commands as the respawned player
	## Usage: function shared/run_respawn_commands {mode:"multiplayer"}
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

