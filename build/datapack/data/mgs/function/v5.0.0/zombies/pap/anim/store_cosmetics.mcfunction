
#> mgs:v5.0.0/zombies/pap/anim/store_cosmetics
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/repap_scope_only with storage mgs:temp _pap_cosm_store
#			mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap_cosm_store
#
# @args		id (unknown)
#

$data modify storage mgs:zombies pap_pending_cosmetics."$(id)" set from storage mgs:temp _pap_cosm_store

