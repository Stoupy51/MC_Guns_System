
#> mgs:v5.0.0/maps/zombies/load
#
# @within	mgs:v5.0.0/maps/zombies/load {id:"map_id",override:{}}
#			mgs:v5.0.0/zombies/load_map_from_storage {id:"$(map_id)",override:{}}
#
# @args		id (string)
#			override (compound)
#

# Load a zombies map by id
# Usage: /function mgs:v5.0.0/maps/zombies/load {id:"map_id",override:{}}
$data modify storage mgs:temp map_load.target set value {id:"$(id)"}
$data modify storage mgs:temp map_load.override set value $(override)

# Copy zombies map list to search through
data modify storage mgs:temp map_load.search set from storage mgs:maps zombies

# Initialize search
scoreboard players set #map_load_idx mgs.data 0
scoreboard players set #map_load_found mgs.data 0
function mgs:v5.0.0/maps/zombies/find_map

