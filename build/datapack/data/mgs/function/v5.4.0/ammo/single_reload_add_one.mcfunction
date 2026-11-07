
#> mgs:v5.4.0/ammo/single_reload_add_one
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/ammo/end_reload
#

execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
scoreboard players add @s mgs.remaining_bullets 1
execute if score @s mgs.remaining_bullets > #capacity mgs.data run scoreboard players operation @s mgs.remaining_bullets = #capacity mgs.data

