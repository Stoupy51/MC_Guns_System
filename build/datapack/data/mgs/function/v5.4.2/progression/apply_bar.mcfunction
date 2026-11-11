
#> mgs:v5.4.2/progression/apply_bar
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/progression/mp/refresh_bar with storage mgs:temp _xp
#			mgs:v5.4.2/progression/zb/refresh_bar with storage mgs:temp _xp
#
# @args		points (unknown)
#			level (unknown)
#

xp set @s 130 levels
$xp set @s $(points) points
$xp set @s $(level) levels

