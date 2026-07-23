
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_start
#
# @within	mgs:v5.1.0/zombies/powerups/activate/fire_sale
#

tag @e[tag=mgs.mystery_box_active] add mgs.mb_orig_active
tag @e[tag=mgs.mystery_box_pos] add mgs.mb_fs_active

# Inactive spots become real temp boxes during the sale — clear their grayed disabled crates first.
kill @e[tag=mgs.mb_disabled]

# Every box is usable now: bring all interaction entities back into reach. This MUST happen before
# the temp boxes are summoned below — a hidden interaction entity is parked 512 blocks under its
# real position (see interaction_hide), and the chest models are summoned `at @s`, so summoning
# first buried every fire-sale chest underground: the box was usable but its model was invisible.
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

execute as @e[tag=mgs.mystery_box_pos,tag=!mgs.mystery_box_active] at @s run function mgs:v5.1.0/zombies/mystery_box/fire_sale_summon_box

