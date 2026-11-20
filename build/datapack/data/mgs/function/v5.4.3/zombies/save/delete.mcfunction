
#> mgs:v5.4.3/zombies/save/delete
#
# @within	mgs:v5.4.3/dialog/close_then
#			string in mgs:v5.4.3/zombies/save/delete_ask {slot:$(slot)}
#
# @args		slot (unknown)
#

$data modify storage mgs:zombies_saves slots[$(slot)] set value {}
function mgs:v5.4.3/zombies/save/load_menu

