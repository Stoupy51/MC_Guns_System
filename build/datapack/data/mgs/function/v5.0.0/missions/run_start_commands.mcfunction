
#> mgs:v5.0.0/missions/run_start_commands
#
# @within	mgs:v5.0.0/missions/end_prep
#

data modify storage mgs:temp _start_cmd_iter set from storage mgs:missions game.map.start_commands
execute if data storage mgs:temp _start_cmd_iter[0] run function mgs:v5.0.0/missions/run_start_commands_iter

