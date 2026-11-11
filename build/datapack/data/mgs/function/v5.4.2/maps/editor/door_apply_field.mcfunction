
#> mgs:v5.4.2/maps/editor/door_apply_field
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/door_set_if_match with storage mgs:temp _door_set
#
# @args		field (unknown)
#

$data modify entity @s data.$(field) set from storage mgs:temp _door_set.value

