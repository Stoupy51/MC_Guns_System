
#> mgs:v5.0.0/zombies/pap/anim/fetch_cosmetics
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/apply_cosmetics with storage mgs:temp _pap_cosm_fetch
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_pending_cosmetics set from storage mgs:zombies pap_pending_cosmetics."$(id)"

