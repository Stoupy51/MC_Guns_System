
#> mgs:v5.0.0/missions/respawn_tp
#
# @executed	at @s
#
# @within	mgs:v5.0.0/missions/actual_respawn
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_mission] run function mgs:v5.0.0/missions/pick_spawn

