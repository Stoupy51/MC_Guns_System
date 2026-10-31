
#> mgs:v5.3.0/maps/editor/name/wallbuy_apply
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/name/wallbuy with storage mgs:temp _ed_name
#
# @args		weapon_id (unknown)
#

$data modify entity @s CustomName set value "Wallbuy $(weapon_id)"

