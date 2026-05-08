
#> mgs:v5.0.1/missions/respawn_tp
#
# @executed	at @s
#
# @within	mgs:v5.0.1/missions/actual_respawn
#			mgs:v5.0.1/missions/join_game
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_mission] run function mgs:v5.0.1/missions/pick_spawn

