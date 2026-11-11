
#> mgs:v5.4.2/maps/editor/name/start_command
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Start Command"
data modify entity @s CustomName set from entity @s data.name

