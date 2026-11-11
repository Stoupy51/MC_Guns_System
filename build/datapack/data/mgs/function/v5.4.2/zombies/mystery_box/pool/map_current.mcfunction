
#> mgs:v5.4.2/zombies/mystery_box/pool/map_current
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/pool/edit_map with storage mgs:zombies game
#
# @args		map_id (unknown)
#

$data modify storage mgs:temp _mb_cur set from storage mgs:maps zombies[{id:"$(map_id)"}].mystery_box_pool

