
#> mgs:v5.4.1/maps/editor/name/mystery_box_pos_apply
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/name/mystery_box_pos with storage mgs:temp _ed_name
#
# @args		location_name (unknown)
#

$data modify entity @s data.name set value "Mystery Box $(location_name)"
data modify entity @s CustomName set from entity @s data.name

