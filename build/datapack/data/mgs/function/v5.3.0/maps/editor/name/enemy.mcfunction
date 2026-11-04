
#> mgs:v5.3.0/maps/editor/name/enemy
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Enemy"
data modify entity @s CustomName set from entity @s data.name

