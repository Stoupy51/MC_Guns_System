
#> mgs:v5.4.1/maps/editor/name/power_switch
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/refresh_marker
#

data modify entity @s data.name set value "Power Switch"
data modify entity @s CustomName set from entity @s data.name

