
#> mgs:v5.3.0/zombies/mystery_box/move_anim_ascend_step
#
# @within	mgs:v5.3.0/zombies/mystery_box/move_anim_tick
#

execute if score #mb_move_timer mgs.data matches 211..251 as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] at @s run function mgs:v5.3.0/zombies/mystery_box/rise_slow
execute if score #mb_move_timer mgs.data matches 211..251 as @e[tag=mgs.mb_bear] at @s run function mgs:v5.3.0/zombies/mystery_box/rise_slow

execute if score #mb_move_timer mgs.data matches 171..210 as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] at @s run function mgs:v5.3.0/zombies/mystery_box/rise_fast
execute if score #mb_move_timer mgs.data matches 171..210 as @e[tag=mgs.mb_bear] at @s run function mgs:v5.3.0/zombies/mystery_box/rise_fast

execute at @n[tag=mgs.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force @a[distance=..48]

