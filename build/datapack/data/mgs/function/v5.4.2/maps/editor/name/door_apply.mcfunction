
#> mgs:v5.4.2/maps/editor/name/door_apply
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/name/door with storage mgs:temp _ed_name
#
# @args		link_id (unknown)
#			price (unknown)
#			rounds (unknown)
#

$data modify entity @s data.name set value "Door link $(link_id) $(price)pts$(rounds)"
data modify entity @s CustomName set from entity @s data.name

