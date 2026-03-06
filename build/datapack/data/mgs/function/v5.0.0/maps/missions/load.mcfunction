
#> mgs:v5.0.0/maps/missions/load
#
# @within	mgs:v5.0.0/missions/load_map_from_storage {id:"$(map_id)",override:{}}
#			mgs:v5.0.0/maps/missions/load {id:"map_id",override:{}}
#
# @args		id (unknown)
#			override (compound)
#

# Load a missions map by id
# Usage: /function mgs:v5.0.0/maps/missions/load {id:"map_id",override:{}}
$data modify storage mgs:temp map_load.target set value {id:"$(id)"}
$data modify storage mgs:temp map_load.override set value $(override)

# Copy missions map list to search through
data modify storage mgs:temp map_load.search set from storage mgs:maps missions

# Initialize search
scoreboard players set #map_load_idx mgs.data 0
scoreboard players set #map_load_found mgs.data 0
function mgs:v5.0.0/maps/missions/find_map

