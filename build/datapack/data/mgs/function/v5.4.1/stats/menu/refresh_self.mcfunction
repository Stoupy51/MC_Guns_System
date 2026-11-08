
#> mgs:v5.4.1/stats/menu/refresh_self
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/menu/fetch
#

data modify storage mgs:temp _st_one set value {}
data modify storage mgs:temp _st_one.uuid set from entity @s UUID
function mgs:v5.4.1/stats/snapshot/by_uuid with storage mgs:temp _st_one

