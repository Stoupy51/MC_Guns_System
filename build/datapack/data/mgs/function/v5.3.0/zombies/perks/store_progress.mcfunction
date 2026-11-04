
#> mgs:v5.3.0/zombies/perks/store_progress
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

$scoreboard players operation @s mgs.zb.perkpaid.$(perk_id) = #pk_paid mgs.data

