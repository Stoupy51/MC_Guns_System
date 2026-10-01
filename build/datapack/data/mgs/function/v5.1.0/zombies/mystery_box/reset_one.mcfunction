
#> mgs:v5.1.0/zombies/mystery_box/reset_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/spin_tick_one
#			mgs:v5.1.0/zombies/mystery_box/show_result_one
#

function mgs:v5.1.0/zombies/mystery_box/close_lid

kill @s

# A Fire Sale that ended during pulls cleans up once none remain.
execute if score #mb_fs_cleanup_pending mgs.data matches 1 unless entity @e[tag=mgs.mb_display] run function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

# A Fire Sale box is hidden again once its pull is done.
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

