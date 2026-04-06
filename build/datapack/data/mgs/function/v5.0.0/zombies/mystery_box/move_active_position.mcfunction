
#> mgs:v5.0.0/zombies/mystery_box/move_active_position
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_transition
#

# Need at least 2 positions to move.
execute store result score #mb_pos_count mgs.data run data get storage mgs:zombies game.map.mystery_box.positions
execute if score #mb_pos_count mgs.data matches ..1 run return 0

tag @e[tag=mgs.mystery_box_active] add mgs.mb_prev_active
tag @e[tag=mgs.mystery_box_active] remove mgs.mystery_box_active
execute as @n[tag=mgs.mystery_box_pos,tag=!mgs.mb_prev_active,sort=random] run tag @s add mgs.mystery_box_active
tag @e[tag=mgs.mb_prev_active] remove mgs.mb_prev_active

