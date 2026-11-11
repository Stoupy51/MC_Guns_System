
#> mgs:v5.4.2/zombies/perks/check_owned
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

scoreboard players set #pk_owned mgs.data 0
$execute if score @s mgs.zb.perk.$(perk_id) matches 1 run scoreboard players set #pk_owned mgs.data 1

