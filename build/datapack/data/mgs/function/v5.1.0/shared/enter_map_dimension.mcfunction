
#> mgs:v5.1.0/shared/enter_map_dimension
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/shared/enter_map with storage mgs:temp _enter
#
# @args		mode (string)
#			map_id (unknown)
#

$data modify storage mgs:temp _enter.dimension set from storage mgs:maps $(mode)[{id:"$(map_id)"}].dimension

