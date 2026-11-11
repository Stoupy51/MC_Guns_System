
#> mgs:v5.4.2/zombies/wallbuys/lookup_weapon
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/wallbuys/on_right_click with storage mgs:temp _wb_buy
#
# @args		id (unknown)
#

$data modify storage mgs:temp _wb_weapon set from storage mgs:zombies wallbuy_data."$(id)"

