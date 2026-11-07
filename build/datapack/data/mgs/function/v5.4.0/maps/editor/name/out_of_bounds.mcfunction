
#> mgs:v5.4.0/maps/editor/name/out_of_bounds
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Out of Bounds"
data modify entity @s CustomName set from entity @s data.name

