
#> mgs:v5.4.1/zombies/spawn_from/special
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/spawn_special_capped
#

scoreboard players set #zb_spawned mgs.data 0
function mgs:v5.4.1/zombies/tag_special_spawns_near_players
execute as @n[type=minecraft:marker,tag=mgs.zb_near,sort=random] at @s run function mgs:v5.4.1/zombies/do_spawn
tag @e[type=minecraft:marker,tag=mgs.zb_near] remove mgs.zb_near

