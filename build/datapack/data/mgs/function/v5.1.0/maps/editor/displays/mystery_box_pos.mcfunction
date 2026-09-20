
#> mgs:v5.1.0/maps/editor/displays/mystery_box_pos
#
# @executed	as @e[tag=mgs.element.mystery_box_pos] & at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[tag=mgs.element.mystery_box_pos] & at @s ]
#

# @s = mystery box marker, at @s
data modify storage mgs:temp _ed_mb.yaw set value 0.0f
data modify storage mgs:temp _ed_mb.yaw set from entity @s data.yaw
execute positioned ^ ^2 ^0.3 run function mgs:v5.1.0/maps/editor/displays/summon_mystery_box with storage mgs:temp _ed_mb

