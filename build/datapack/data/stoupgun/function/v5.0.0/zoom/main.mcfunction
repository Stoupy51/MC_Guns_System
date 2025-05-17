
#> stoupgun:v5.0.0/zoom/main
#
# @within	stoupgun:v5.0.0/player/tick
#

# If no gun data, stop here
execute unless data storage stoupgun:gun stats run return run function stoupgun:v5.0.0/zoom/check_slowness

# If already zoom and not sneaking, unzoom
execute if data storage stoupgun:gun stats.is_zoom unless predicate stoupgun:v5.0.0/is_sneaking run return run function stoupgun:v5.0.0/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage stoupgun:gun stats.is_zoom if predicate stoupgun:v5.0.0/is_sneaking run return run function stoupgun:v5.0.0/zoom/set

