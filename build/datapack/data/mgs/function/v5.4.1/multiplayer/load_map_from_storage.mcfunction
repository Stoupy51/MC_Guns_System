
#> mgs:v5.4.1/multiplayer/load_map_from_storage
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/start with storage mgs:multiplayer game
#
# @args		map_id (unknown)
#

data remove storage mgs:temp map_load
$execute store success score #map_load_found mgs.data run data modify storage mgs:temp map_load.result set from storage mgs:maps multiplayer[{id:"$(map_id)"}]

