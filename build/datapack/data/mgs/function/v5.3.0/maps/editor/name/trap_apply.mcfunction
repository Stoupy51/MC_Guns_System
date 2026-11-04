
#> mgs:v5.3.0/maps/editor/name/trap_apply
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/name/trap with storage mgs:temp _ed_name
#
# @args		type (unknown)
#

$data modify entity @s data.name set value "Trap type $(type)"
data modify entity @s CustomName set from entity @s data.name

