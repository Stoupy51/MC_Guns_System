
#> mgs:v5.4.2/maps/editor/name/enemy
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Enemy"
data modify entity @s CustomName set from entity @s data.name

