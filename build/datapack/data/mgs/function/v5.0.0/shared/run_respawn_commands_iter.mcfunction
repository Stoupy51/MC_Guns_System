
#> mgs:v5.0.0/shared/run_respawn_commands_iter
#
# @executed	at @s
#
# @within	mgs:v5.0.0/shared/run_respawn_commands [ at @s ]
#			mgs:v5.0.0/shared/run_respawn_commands_iter [ at @s ]
#

# Copy command string
data modify storage mgs:temp _respawn_cmd.command set from storage mgs:temp _respawn_cmd_iter[0].command

# Execute as current player and advance
function mgs:v5.0.0/shared/run_respawn_command with storage mgs:temp _respawn_cmd
data remove storage mgs:temp _respawn_cmd_iter[0]
execute if data storage mgs:temp _respawn_cmd_iter[0] at @s run function mgs:v5.0.0/shared/run_respawn_commands_iter

