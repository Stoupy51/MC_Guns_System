
#> mgs:v5.4.2/zombies/pap/anim/store_cosmetics
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/pap/repap_scope_only with storage mgs:temp _pap_cosm_store
#			mgs:v5.4.2/zombies/pap/on_right_click with storage mgs:temp _pap_cosm_store
#
# @args		id (unknown)
#

$data modify storage mgs:zombies pap_pending_cosmetics."$(id)" set from storage mgs:temp _pap_cosm_store

