
#> mgs:v5.4.1/maps/editor/name/perk_machine_apply
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/name/perk_machine with storage mgs:temp _ed_name
#
# @args		perk_id (unknown)
#

$data modify entity @s data.name set value "Perk Machine $(perk_id)"
data modify entity @s CustomName set from entity @s data.name

