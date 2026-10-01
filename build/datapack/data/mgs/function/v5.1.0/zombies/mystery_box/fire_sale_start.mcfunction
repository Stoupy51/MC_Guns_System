
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_start
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/powerups/activate/fire_sale
#

tag @e[tag=mgs.mystery_box_active] add mgs.mb_orig_active
tag @e[tag=mgs.mystery_box_pos] add mgs.mb_fs_active

# The inactive spots become real boxes, so their grayed crates go.
kill @e[tag=mgs.mb_disabled]

# Before summoning the boxes: a hidden interaction entity sits 512 blocks under its spot, and the chests are summoned `at @s`.
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

execute as @e[tag=mgs.mystery_box_pos,tag=!mgs.mystery_box_active] at @s run function mgs:v5.1.0/zombies/mystery_box/fire_sale_summon_box

