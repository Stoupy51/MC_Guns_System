
#> mgs:v5.3.0/stats/menu/players_uuid
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_next with storage mgs:temp _sp
#
# @args		i (unknown)
#

$data modify storage mgs:temp _sp.uuid set from storage mgs:stats known[$(i)]
function mgs:v5.3.0/stats/menu/players_name with storage mgs:temp _sp

