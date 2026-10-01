
#> mgs:v5.1.0/zombies/wunderfizz/move_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

scoreboard players remove #wf_move_timer mgs.data 1

execute if score #wf_move_timer mgs.data matches 56.. as @e[tag=mgs.wf_bear] at @s run tp @s ~ ~0.06 ~

# Midpoint: model swap and interaction visibility.
execute if score #wf_move_timer mgs.data matches 55 run function mgs:v5.1.0/zombies/wunderfizz/do_relocate

execute if score #wf_move_timer mgs.data matches 48 as @e[tag=mgs.wf_bear] at @s run particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 15 force @a[distance=..48]
execute if score #wf_move_timer mgs.data matches 48 run kill @e[tag=mgs.wf_bear]

execute if score #wf_move_timer mgs.data matches 0 run function mgs:v5.1.0/zombies/wunderfizz/move_land

