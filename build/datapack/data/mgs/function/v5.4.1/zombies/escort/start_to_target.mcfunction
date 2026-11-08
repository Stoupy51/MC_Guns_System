
#> mgs:v5.4.1/zombies/escort/start_to_target
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/arrival/land [ as @n[tag=mgs.zb_new_root] & at @s ]
#			mgs:v5.4.1/zombies/zombie_finish_rise
#

execute if score #zb_escort_count mgs.data matches 16.. run return 0
scoreboard players set #zb_escort_mode mgs.data 2
function mgs:v5.4.1/zombies/escort/start

