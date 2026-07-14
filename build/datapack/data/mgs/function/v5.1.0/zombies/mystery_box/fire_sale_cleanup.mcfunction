
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup
#
# @within	mgs:v5.1.0/zombies/mystery_box/fire_sale_end
#			mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#			mgs:v5.1.0/zombies/mystery_box/collect
#			mgs:v5.1.0/zombies/mystery_box/reset_one
#

# Remove every temporary box and clear Fire-Sale bookkeeping. The active box never changes during
# a Fire Sale, so we must NOT touch the mystery_box_active tag here (doing so could strip it off
# every box if state is inconsistent, leaving no usable box).
tag @e[tag=mgs.mb_orig_active] remove mgs.mb_orig_active
kill @e[tag=mgs.mb_temp]
scoreboard players set #mb_fs_cleanup_pending mgs.data 0

# Non-active boxes are dead again: tuck their interaction entities away
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

