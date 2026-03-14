
#> mgs:v5.0.0/zombies/wallbuys/get_hover_name
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_hover_enter with storage mgs:temp _wb_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp wb_hover_name set from storage mgs:zombies wallbuy_data."$(id)".name

