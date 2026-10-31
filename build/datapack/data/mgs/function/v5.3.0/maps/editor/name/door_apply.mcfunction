
#> mgs:v5.3.0/maps/editor/name/door_apply
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/name/door with storage mgs:temp _ed_name
#
# @args		link_id (unknown)
#			price (unknown)
#			rounds (unknown)
#

$data modify entity @s CustomName set value "Door link $(link_id) $(price)pts$(rounds)"

