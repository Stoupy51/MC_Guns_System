
#> mgs:v5.0.0/zombies/pap/lookup_machine
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_hover with storage mgs:temp _pap_hover
#			mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_machine set from storage mgs:zombies pap_data."$(id)"

