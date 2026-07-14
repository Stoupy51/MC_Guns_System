
#> mgs:v5.1.0/zombies/mystery_box/reset_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/spin_tick_one
#			mgs:v5.1.0/zombies/mystery_box/show_result_one
#

# Close this box's lid
function mgs:v5.1.0/zombies/mystery_box/close_lid

# Remove the display (buyer is tracked per-display, nothing to clear on the player)
kill @s

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending mgs.data matches 1 unless entity @e[tag=mgs.mb_display] run function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

# This box's pull ended: if it's no longer usable (e.g. a Fire-Sale box after the sale), hide it
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

