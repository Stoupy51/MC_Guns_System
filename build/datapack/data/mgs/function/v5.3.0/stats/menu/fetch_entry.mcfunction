
#> mgs:v5.3.0/stats/menu/fetch_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/fetch with storage mgs:temp _sv
#
# @args		uuid (unknown)
#

$data modify storage mgs:temp _sv.p set from storage mgs:stats players."$(uuid)"

