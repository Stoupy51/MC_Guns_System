
#> mgs:v5.4.1/zombies/pap/lookup_machine
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/pap/on_hover with storage mgs:temp _pap_hover
#			mgs:v5.4.1/zombies/pap/on_right_click with storage mgs:temp _pap_hover
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_machine set from storage mgs:zombies pap_data."$(id)"

