
#> mgs:v5.4.2/zombies/save/menu_name
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/save_menu with storage mgs:temp _sv_name
#
# @args		map_id (unknown)
#			round (unknown)
#

$data modify storage mgs:temp dialog.inputs[0].initial set value "$(map_id) r$(round)"

