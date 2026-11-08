
#> mgs:v5.4.1/missions/load_map_from_storage
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/missions/start with storage mgs:missions game
#
# @args		map_id (unknown)
#

data remove storage mgs:temp map_load
$execute store success score #map_load_found mgs.data run data modify storage mgs:temp map_load.result set from storage mgs:maps missions[{id:"$(map_id)"}]

