
#> mgs:v5.3.0/zombies/spawn_from/zombies
#
# @within	mgs:v5.3.0/zombies/spawn_batch_tick
#

scoreboard players set #zb_spawned mgs.data 0
function mgs:v5.3.0/zombies/tag_zombies_spawns_near_players
execute as @n[type=minecraft:marker,tag=mgs.zb_near,sort=random] at @s run function mgs:v5.3.0/zombies/do_spawn
tag @e[type=minecraft:marker,tag=mgs.zb_near] remove mgs.zb_near

