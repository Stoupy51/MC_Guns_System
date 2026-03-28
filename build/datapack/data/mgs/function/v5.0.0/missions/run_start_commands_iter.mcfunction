
#> mgs:v5.0.0/missions/run_start_commands_iter
#
# @within	mgs:v5.0.0/missions/run_start_commands
#			mgs:v5.0.0/missions/run_start_commands_iter
#

# Read relative position
execute store result score #cx mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[0]
execute store result score #cy mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[1]
execute store result score #cz mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[2]

# Convert to absolute
scoreboard players operation #cx mgs.data += #gm_base_x mgs.data
scoreboard players operation #cy mgs.data += #gm_base_y mgs.data
scoreboard players operation #cz mgs.data += #gm_base_z mgs.data

# Prepare macro args
execute store result storage mgs:temp _start_cmd.x int 1 run scoreboard players get #cx mgs.data
execute store result storage mgs:temp _start_cmd.y int 1 run scoreboard players get #cy mgs.data
execute store result storage mgs:temp _start_cmd.z int 1 run scoreboard players get #cz mgs.data
data modify storage mgs:temp _start_cmd.command set from storage mgs:temp _start_cmd_iter[0].command

# Execute and advance
function mgs:v5.0.0/missions/run_start_command with storage mgs:temp _start_cmd
data remove storage mgs:temp _start_cmd_iter[0]
execute if data storage mgs:temp _start_cmd_iter[0] run function mgs:v5.0.0/missions/run_start_commands_iter

