
#> mgs:v5.4.0/maps/editor/displays/power_switch
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/refresh_displays [ at @s ]
#

# Run as the power switch marker, at it.
data modify storage mgs:temp _ed_ps.yaw set value 0.0f
data modify storage mgs:temp _ed_ps.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~.5 ~.5 run function mgs:v5.4.0/maps/editor/displays/summon_power_switch with storage mgs:temp _ed_ps

