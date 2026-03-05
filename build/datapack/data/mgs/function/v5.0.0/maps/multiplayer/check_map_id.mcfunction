
#> mgs:v5.0.0/maps/multiplayer/check_map_id
#
# @within	mgs:v5.0.0/maps/multiplayer/find_map with storage mgs:temp map_load.target_id
#
# @args		id (unknown)
#

$execute store success score #map_load_found mgs.data if data storage mgs:temp map_load{check:{id:"$(id)"}}
execute if score #map_load_found mgs.data matches 1 run data modify storage mgs:temp map_load.result set from storage mgs:temp map_load.check

# Apply base_coordinates override if present
execute if score #map_load_found mgs.data matches 1 if data storage mgs:temp map_load.override.base_coordinates run data modify storage mgs:temp map_load.result.base_coordinates set from storage mgs:temp map_load.override.base_coordinates

