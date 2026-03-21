
#> mgs:v5.0.0/maps/multiplayer/load
#
# @within	mgs:v5.0.0/multiplayer/load_map_from_storage {id:"$(map_id)",override:{}}
#			mgs:v5.0.0/maps/multiplayer/load {id:"map_id",override:{}}
#
# @args		id (string)
#			override (compound)
#

# Load a map for gameplay or editing
# Usage: /function mgs:v5.0.0/maps/multiplayer/load {id:"map_id",override:{}}
# Override can contain: dimension:"minecraft:overworld", base_coordinates:[x,y,z]

# Store the target ID for search
$data modify storage mgs:temp map_load.target set value {id:"$(id)"}
$data modify storage mgs:temp map_load.override set value $(override)

# Copy full map list to search through
data modify storage mgs:temp map_load.search set from storage mgs:maps multiplayer

# Initialize search
scoreboard players set #map_load_idx mgs.data 0
scoreboard players set #map_load_found mgs.data 0
function mgs:v5.0.0/maps/multiplayer/find_map

