
#> mgs:v5.0.0/shared/maps/find_map
#
# @within	mgs:v5.0.0/shared/maps/load
#			mgs:v5.0.0/shared/maps/find_map
#

execute unless data storage mgs:temp map_load.search[0] run return fail

data modify storage mgs:temp map_load.check set from storage mgs:temp map_load.search[0]
function mgs:v5.0.0/shared/maps/check_map_id with storage mgs:temp map_load.target

execute if score #map_load_found mgs.data matches 1 run return 1

data remove storage mgs:temp map_load.search[0]
scoreboard players add #map_load_idx mgs.data 1
function mgs:v5.0.0/shared/maps/find_map

