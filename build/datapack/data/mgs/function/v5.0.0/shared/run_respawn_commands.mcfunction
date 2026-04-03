
#> mgs:v5.0.0/shared/run_respawn_commands
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/actual_respawn {mode:"multiplayer"} [ at @s ]
#			mgs:v5.0.0/missions/actual_respawn {mode:"missions"} [ at @s ]
#
# @args		mode (string)
#

$data modify storage mgs:temp _respawn_cmd_iter set from storage mgs:$(mode) game.map.respawn_commands
execute if data storage mgs:temp _respawn_cmd_iter[0] at @s run function mgs:v5.0.0/shared/run_respawn_commands_iter

