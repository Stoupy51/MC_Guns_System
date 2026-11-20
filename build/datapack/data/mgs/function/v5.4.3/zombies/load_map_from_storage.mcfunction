
#> mgs:v5.4.3/zombies/load_map_from_storage
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/zombies/start with storage mgs:zombies game
#			mgs:v5.4.3/zombies/save/load with storage mgs:temp _sv_map
#
# @args		map_id (unknown)
#

data remove storage mgs:temp map_load
$execute store success score #map_load_found mgs.data run data modify storage mgs:temp map_load.result set from storage mgs:maps zombies[{id:"$(map_id)"}]

