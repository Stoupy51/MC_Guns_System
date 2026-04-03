
#> mgs:v5.0.0/zombies/doors/get_hover_name
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.0.0/zombies/doors/on_right_click with storage mgs:temp _door_hover
#			mgs:v5.0.0/zombies/doors/on_hover with storage mgs:temp _door_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _door_hover_name set from storage mgs:zombies door_names."$(id)".name

