
#> mgs:v5.0.0/zombies/doors/get_hover_name_back
#
# @within	mgs:v5.0.0/zombies/doors/on_hover with storage mgs:temp _door_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _door_hover_name set from storage mgs:zombies door_names."$(id)".back_name

