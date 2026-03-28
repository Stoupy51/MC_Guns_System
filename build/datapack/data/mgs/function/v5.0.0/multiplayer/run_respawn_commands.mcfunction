
#> mgs:v5.0.0/multiplayer/run_respawn_commands
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/actual_respawn [ at @s ]
#

data modify storage mgs:temp _respawn_cmd_iter set from storage mgs:multiplayer game.map.respawn_commands
execute if data storage mgs:temp _respawn_cmd_iter[0] at @s run function mgs:v5.0.0/multiplayer/run_respawn_commands_iter

