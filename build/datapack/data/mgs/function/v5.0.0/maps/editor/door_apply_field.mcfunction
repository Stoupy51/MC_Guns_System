
#> mgs:v5.0.0/maps/editor/door_apply_field
#
# @executed	as @e[tag=mgs.element.door]
#
# @within	mgs:v5.0.0/maps/editor/door_set_if_match with storage mgs:temp _door_set
#
# @args		field (unknown)
#

$data modify entity @s data.$(field) set from storage mgs:temp _door_set.value

