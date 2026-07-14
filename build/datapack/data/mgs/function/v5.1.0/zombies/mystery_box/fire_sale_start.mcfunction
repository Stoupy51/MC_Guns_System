
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_start
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.1.0/zombies/powerups/activate/fire_sale
#

tag @e[tag=mgs.mystery_box_active] add mgs.mb_orig_active
tag @e[tag=mgs.mystery_box_pos] add mgs.mb_fs_active
execute as @e[tag=mgs.mystery_box_pos,tag=!mgs.mystery_box_active] at @s run function mgs:v5.1.0/zombies/mystery_box/fire_sale_summon_box

