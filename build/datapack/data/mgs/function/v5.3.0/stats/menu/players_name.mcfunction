
#> mgs:v5.3.0/stats/menu/players_name
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_uuid with storage mgs:temp _sp
#
# @args		uuid (unknown)
#			kind (unknown)
#

$data modify storage mgs:temp _sp.name set from storage mgs:stats players."$(uuid)".name
$function mgs:v5.3.0/stats/menu/players_button_$(kind) with storage mgs:temp _sp

