
#> mgs:v5.1.0/zombies/barriers/compute_brightness
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.barrier_display] & at @s ]
#			mgs:v5.1.0/zombies/barriers/setup_iter [ as @n[tag=mgs._barrier_new_d] & at @s ]
#

# Reset light score, then sample own position and all 6 neighbors (stop early at 15)
scoreboard players set #light mgs.data 0
execute if score #light mgs.data matches ..14 positioned ~ ~ ~ run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~ ~1 ~ run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~ ~-1 ~ run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~1 ~ ~ run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~-1 ~ ~ run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~ ~ ~1 run function mgs:v5.1.0/zombies/barriers/check_light
execute if score #light mgs.data matches ..14 positioned ~ ~ ~-1 run function mgs:v5.1.0/zombies/barriers/check_light

# Apply computed brightness to the display
data merge entity @s {brightness:{block:0,sky:0}}
execute store result entity @s brightness.block int 1 run scoreboard players get #light mgs.data
execute store result entity @s brightness.sky int 1 run scoreboard players get #light mgs.data

