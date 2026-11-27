
#> mgs:v5.4.4/dialog/close_then
#
# @within	mgs:v5.4.4/dialog/close_then
#			string in mgs:v5.4.4/zombies/save/load_row_add {run:\"zombies/save/load {slot:$(slot)}\"}
#			dialog mgs:v5.4.4/config
#			dialog mgs:v5.4.4/zombies/setup
#			dialog mgs:v5.4.4/multiplayer/setup
#			dialog mgs:v5.4.4/missions/setup
#
# @args		run (string)
#

dialog clear @s
$function mgs:v5.4.4/$(run)

