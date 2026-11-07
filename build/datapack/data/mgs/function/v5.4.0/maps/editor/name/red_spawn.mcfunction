
#> mgs:v5.4.0/maps/editor/name/red_spawn
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Red Spawn"
data modify entity @s CustomName set from entity @s data.name

