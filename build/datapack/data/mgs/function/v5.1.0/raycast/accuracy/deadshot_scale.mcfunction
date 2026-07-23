
#> mgs:v5.1.0/raycast/accuracy/deadshot_scale
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/shoot
#

execute store result score #ds_acc mgs.data run data get storage mgs:gun accuracy 1000
scoreboard players set #ds_num mgs.data 65
scoreboard players set #ds_den mgs.data 100
scoreboard players operation #ds_acc mgs.data *= #ds_num mgs.data
scoreboard players operation #ds_acc mgs.data /= #ds_den mgs.data
execute store result storage mgs:gun accuracy double 0.001 run scoreboard players get #ds_acc mgs.data

