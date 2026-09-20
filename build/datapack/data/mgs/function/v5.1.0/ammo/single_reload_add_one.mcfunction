
#> mgs:v5.1.0/ammo/single_reload_add_one
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/end_reload
#

execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
scoreboard players add @s mgs.remaining_bullets 1
execute if score @s mgs.remaining_bullets > #capacity mgs.data run scoreboard players operation @s mgs.remaining_bullets = #capacity mgs.data

