
#> mgs:v5.4.0/maps/editor/name/general_spawn
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/refresh_marker
#

data modify entity @s data.name set value "General Spawn"
data modify entity @s CustomName set from entity @s data.name

