
#> mgs:v5.4.3/dialog/close_then
#
# @within	mgs:v5.4.3/dialog/close_then
#			string in mgs:v5.4.3/zombies/save/load_row_add {run:\"zombies/save/load {slot:$(slot)}\"}
#			dialog mgs:v5.4.3/config
#			dialog mgs:v5.4.3/zombies/setup
#			dialog mgs:v5.4.3/multiplayer/setup
#			dialog mgs:v5.4.3/missions/setup
#
# @args		run (string)
#

dialog clear @s
$function mgs:v5.4.3/$(run)

