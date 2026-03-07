
#> mgs:v5.0.0/missions/respawn_tp
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/missions/on_respawn
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_mission] run function mgs:v5.0.0/missions/pick_spawn

