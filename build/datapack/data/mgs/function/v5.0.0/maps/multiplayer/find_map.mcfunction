
#> mgs:v5.0.0/maps/multiplayer/find_map
#
# @within	mgs:v5.0.0/maps/multiplayer/load
#			mgs:v5.0.0/maps/multiplayer/find_map
#

# Check if the list still has elements
execute unless data storage mgs:temp map_load.search[0] run return fail

# Copy first element to check
data modify storage mgs:temp map_load.check set from storage mgs:temp map_load.search[0]

# Use macro to compare IDs
function mgs:v5.0.0/maps/multiplayer/check_map_id with storage mgs:temp map_load.target_id

# If found, stop
execute if score #map_load_found mgs.data matches 1 run return 1

# Not found, advance to next
data remove storage mgs:temp map_load.search[0]
scoreboard players add #map_load_idx mgs.data 1
function mgs:v5.0.0/maps/multiplayer/find_map

