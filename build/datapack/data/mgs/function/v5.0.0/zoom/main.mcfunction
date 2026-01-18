
#> mgs:v5.0.0/zoom/main
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# If no gun data, stop here
execute unless data storage mgs:gun all.stats run return run function mgs:v5.0.0/zoom/check_slowness

# If already zoom and not sneaking, unzoom
execute if data storage mgs:gun all.stats.is_zoom unless predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage mgs:gun all.stats.is_zoom if predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/set

