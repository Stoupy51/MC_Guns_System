
#> mgs:v5.0.0/zombies/doors/get_hover_name
#
# @within	mgs:v5.0.0/zombies/doors/on_hover_enter with storage mgs:temp _door_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _door_hover_name set from storage mgs:zombies door_names."$(id)".name

