
#> mgs:v5.3.0/zombies/mystery_box/pool/map_current
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/mystery_box/pool/edit_map with storage mgs:zombies game
#
# @args		map_id (unknown)
#

$data modify storage mgs:temp _mb_cur set from storage mgs:maps zombies[{id:"$(map_id)"}].mystery_box_pool

