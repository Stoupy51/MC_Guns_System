
#> mgs:v5.4.1/zombies/pap/anim/fetch_cosmetics
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/pap/anim/apply_cosmetics with storage mgs:temp _pap_cosm_fetch
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_pending_cosmetics set from storage mgs:zombies pap_pending_cosmetics."$(id)"

