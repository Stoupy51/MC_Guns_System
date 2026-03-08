
#> mgs:v5.0.0/zombies/doors/store_name
#
# @within	mgs:v5.0.0/zombies/doors/setup_iter with storage mgs:temp _door_name
#
# @args		id (unknown)
#			name (unknown)
#			back_name (unknown)
#

$data modify storage mgs:zombies door_names."$(id)" set value {name:"$(name)",back_name:"$(back_name)"}

