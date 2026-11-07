
#> mgs:v5.4.0/stats/menu/players_uuid
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/menu/players_next with storage mgs:temp _sp
#
# @args		i (unknown)
#

$data modify storage mgs:temp _sp.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.4.0/stats/menu/players_name with storage mgs:temp _sp

