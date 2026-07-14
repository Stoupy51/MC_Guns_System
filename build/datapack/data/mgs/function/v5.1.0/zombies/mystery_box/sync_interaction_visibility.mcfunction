
#> mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility
#
# @within	mgs:v5.1.0/zombies/mystery_box/setup_positions
#			mgs:v5.1.0/zombies/mystery_box/fire_sale_start
#			mgs:v5.1.0/zombies/mystery_box/fire_sale_end
#			mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup
#			mgs:v5.1.0/zombies/mystery_box/move_anim_transition
#			mgs:v5.1.0/zombies/mystery_box/collect
#			mgs:v5.1.0/zombies/mystery_box/reset_one
#

execute as @e[tag=mgs.mystery_box_pos] at @s run function mgs:v5.1.0/zombies/mystery_box/sync_interaction_one

