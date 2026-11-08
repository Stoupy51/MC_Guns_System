
#> mgs:v5.4.1/dialog/close_then
#
# @within	mgs:v5.4.1/dialog/close_then
#			dialog mgs:v5.4.1/config
#			dialog mgs:v5.4.1/zombies/setup
#			dialog mgs:v5.4.1/multiplayer/setup
#			dialog mgs:v5.4.1/missions/setup
#
# @args		run (unknown)
#

dialog clear @s
$function mgs:v5.4.1/$(run)

