
#> mgs:v5.0.0/missions/run_respawn_commands
#
# @executed	at @s
#
# @within	mgs:v5.0.0/missions/actual_respawn [ at @s ]
#

data modify storage mgs:temp _respawn_cmd_iter set from storage mgs:missions game.map.respawn_commands
execute if data storage mgs:temp _respawn_cmd_iter[0] at @s run function mgs:v5.0.0/missions/run_respawn_commands_iter

