
#> mgs:v5.0.0/shared/maps/load
#
# @within	mgs:v5.0.0/zombies/load_map_from_storage {id:"$(map_id)",mode:"zombies",override:{}}
#			mgs:v5.0.0/multiplayer/load_map_from_storage {id:"$(map_id)",mode:"multiplayer",override:{}}
#			mgs:v5.0.0/missions/load_map_from_storage {id:"$(map_id)",mode:"missions",override:{}}
#
# @args		id (string)
#			override (compound)
#			mode (string)
#

$data modify storage mgs:temp map_load.target set value {id:"$(id)"}
$data modify storage mgs:temp map_load.override set value $(override)
$data modify storage mgs:temp map_load.search set from storage mgs:maps $(mode)

scoreboard players set #map_load_idx mgs.data 0
scoreboard players set #map_load_found mgs.data 0
function mgs:v5.0.0/shared/maps/find_map

