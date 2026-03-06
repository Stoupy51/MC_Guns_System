
#> mgs:v5.0.0/missions/tp_to_spawn
#
# @executed	as @e[tag=mgs.spawn_candidate,sort=random,limit=1]
#
# @within	mgs:v5.0.0/missions/pick_spawn [ as @e[tag=mgs.spawn_candidate,sort=random,limit=1] ]
#

execute store result storage mgs:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage mgs:temp _tp.yaw set from entity @s data.yaw

execute as @p[tag=mgs.spawn_pending] run function mgs:v5.0.0/missions/tp_player_at with storage mgs:temp _tp

execute unless data storage mgs:missions game{state:"active"} run tag @s add mgs.spawn_used

