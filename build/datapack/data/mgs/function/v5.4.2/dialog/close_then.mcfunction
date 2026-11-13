
#> mgs:v5.4.2/dialog/close_then
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/zombies/save/load_row_add {run:\"zombies/save/load {slot:$(slot)}\"}
#			dialog mgs:v5.4.2/config
#			dialog mgs:v5.4.2/zombies/setup
#			dialog mgs:v5.4.2/multiplayer/setup
#			dialog mgs:v5.4.2/missions/setup
#
# @args		run (string)
#

dialog clear @s
$function mgs:v5.4.2/$(run)

