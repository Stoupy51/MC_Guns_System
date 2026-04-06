
#> mgs:v5.0.0/zombies/mystery_box/move_anim_descend_step
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_tick
#

# Fast phase (first half): descend ~0.18 blocks/tick
execute if score #mb_move_timer mgs.data matches 35..69 as @n[tag=mgs.mb_presence] at @s run tp @s ~ ~-0.18 ~

# Slow phase (second half, landing): descend ~0.06 blocks/tick
execute if score #mb_move_timer mgs.data matches 1..34 as @n[tag=mgs.mb_presence] at @s run tp @s ~ ~-0.06 ~

# Trailing particles
execute at @n[tag=mgs.mb_presence] run particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.1 0.2 0.01 1 force

