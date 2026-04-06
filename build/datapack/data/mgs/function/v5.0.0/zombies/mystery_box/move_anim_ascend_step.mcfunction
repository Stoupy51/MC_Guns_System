
#> mgs:v5.0.0/zombies/mystery_box/move_anim_ascend_step
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_tick
#

# Slow phase (first half): rise ~0.06 blocks/tick
execute if score #mb_move_timer mgs.data matches 211..251 as @n[tag=mgs.mb_presence] at @s run tp @s ~ ~0.06 ~
execute if score #mb_move_timer mgs.data matches 211..251 as @n[tag=mgs.mb_display] at @s run tp @s ~ ~0.06 ~

# Fast phase (second half): rise ~0.18 blocks/tick
execute if score #mb_move_timer mgs.data matches 171..210 as @n[tag=mgs.mb_presence] at @s run tp @s ~ ~0.18 ~
execute if score #mb_move_timer mgs.data matches 171..210 as @n[tag=mgs.mb_display] at @s run tp @s ~ ~0.18 ~

# Smoke particles at old location
execute at @n[tag=mgs.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force

