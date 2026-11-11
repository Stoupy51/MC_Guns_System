
#> mgs:v5.4.2/zombies/pap/anim/store_slot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/pap/anim/start with storage mgs:temp _pap_anim_slot
#
# @args		id (unknown)
#			slot (unknown)
#

$data modify storage mgs:zombies pap_anim_slot."$(id)" set value "$(slot)"

