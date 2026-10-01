
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup
#
# @within	mgs:v5.1.0/zombies/mystery_box/fire_sale_end
#			mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#			mgs:v5.1.0/zombies/mystery_box/collect
#			mgs:v5.1.0/zombies/mystery_box/reset_one
#

# The active box never changes during a Fire Sale, so its tag is left alone.
tag @e[tag=mgs.mb_orig_active] remove mgs.mb_orig_active
kill @e[tag=mgs.mb_temp]
scoreboard players set #mb_fs_cleanup_pending mgs.data 0

function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

function mgs:v5.1.0/zombies/mystery_box/refresh_disabled

