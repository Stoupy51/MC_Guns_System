
#> mgs:v5.0.0/zombies/run_start_commands
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

data modify storage mgs:temp _start_cmd_iter set from storage mgs:zombies game.map.start_commands
execute if data storage mgs:temp _start_cmd_iter[0] run function mgs:v5.0.0/zombies/run_start_commands_iter

