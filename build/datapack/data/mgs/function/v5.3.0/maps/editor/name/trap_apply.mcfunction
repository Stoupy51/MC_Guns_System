
#> mgs:v5.3.0/maps/editor/name/trap_apply
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/name/trap with storage mgs:temp _ed_name
#
# @args		type (unknown)
#

$data modify entity @s CustomName set value "Trap type $(type)"

