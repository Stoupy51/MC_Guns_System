
#> mgs:v5.0.0/zombies/pap/store_data
#
# @within	mgs:v5.0.0/zombies/pap/setup_iter with storage mgs:temp _pap_store
#
# @args		id (unknown)
#			name (unknown)
#

$data modify storage mgs:zombies pap_data."$(id)" set value {name:"$(name)"}

