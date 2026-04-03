
#> mgs:v5.0.0/zombies/wallbuys/get_hover_name
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_hover with storage mgs:temp _wb_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _wb_weapon set from storage mgs:zombies wallbuy_data."$(id)"

