
#> mgs:v5.1.0/missions/load_map_from_storage
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/missions/start with storage mgs:missions game
#
# @args		map_id (unknown)
#

$function mgs:v5.1.0/shared/maps/load {id:"$(map_id)",mode:"missions",override:{}}

