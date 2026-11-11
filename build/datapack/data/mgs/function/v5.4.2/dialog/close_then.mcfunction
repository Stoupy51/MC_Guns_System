
#> mgs:v5.4.2/dialog/close_then
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/config
#			dialog mgs:v5.4.2/zombies/setup
#			dialog mgs:v5.4.2/multiplayer/setup
#			dialog mgs:v5.4.2/missions/setup
#
# @args		run (unknown)
#

dialog clear @s
$function mgs:v5.4.2/$(run)

