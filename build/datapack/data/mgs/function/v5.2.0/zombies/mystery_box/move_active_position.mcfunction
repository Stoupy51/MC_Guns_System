
#> mgs:v5.2.0/zombies/mystery_box/move_active_position
#
# @within	mgs:v5.2.0/zombies/mystery_box/move_anim_transition
#

tag @e[tag=mgs.mystery_box_active] add mgs.mb_prev_active
tag @e[tag=mgs.mystery_box_active] remove mgs.mystery_box_active
execute as @n[tag=mgs.mystery_box_pos,tag=!mgs.mb_prev_active,sort=random] run tag @s add mgs.mystery_box_active
tag @e[tag=mgs.mb_prev_active] remove mgs.mb_prev_active

