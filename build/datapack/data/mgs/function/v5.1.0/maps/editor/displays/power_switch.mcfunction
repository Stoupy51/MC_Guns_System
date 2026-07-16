
#> mgs:v5.1.0/maps/editor/displays/power_switch
#
# @executed	as @e[tag=mgs.element.power_switch] & at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[tag=mgs.element.power_switch] & at @s ]
#

# @s = power switch marker, at @s
data modify storage mgs:temp _ed_ps.yaw set value 0.0f
data modify storage mgs:temp _ed_ps.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~.5 ~.5 run function mgs:v5.1.0/maps/editor/displays/summon_power_switch with storage mgs:temp _ed_ps

