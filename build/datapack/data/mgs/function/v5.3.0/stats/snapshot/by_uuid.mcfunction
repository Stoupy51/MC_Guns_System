
#> mgs:v5.3.0/stats/snapshot/by_uuid
#
# @within	mgs:v5.3.0/stats/snapshot/roster_next with storage mgs:temp _st_one
#			mgs:v5.3.0/stats/menu/refresh_self with storage mgs:temp _st_one
#
# @args		uuid (unknown)
#

$data modify storage mgs:temp _st_one.name set from storage mgs:stats players."$(uuid)".name
function mgs:v5.3.0/stats/snapshot/player with storage mgs:temp _st_one

