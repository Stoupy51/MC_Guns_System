
#> mgs:v5.3.0/stats/menu/refresh_self
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/fetch
#

data modify storage mgs:temp _st_one set value {}
data modify storage mgs:temp _st_one.uuid set from entity @s UUID
function mgs:v5.3.0/stats/snapshot/by_uuid with storage mgs:temp _st_one

