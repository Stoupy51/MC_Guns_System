
#> mgs:v5.4.2/zombies/save/load_row
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/load_menu with storage mgs:temp _sv_row
#
# @args		slot (int)
#

$data modify storage mgs:temp _sv_row.name set from storage mgs:zombies_saves slots[$(slot)].name
$data modify storage mgs:temp _sv_row.map_id set from storage mgs:zombies_saves slots[$(slot)].map_id
$data modify storage mgs:temp _sv_row.round set from storage mgs:zombies_saves slots[$(slot)].round
function mgs:v5.4.2/zombies/save/load_row_add with storage mgs:temp _sv_row

