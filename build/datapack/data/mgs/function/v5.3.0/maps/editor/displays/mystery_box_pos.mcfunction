
#> mgs:v5.3.0/maps/editor/displays/mystery_box_pos
#
# @executed	at @s
#
# @within	mgs:v5.3.0/maps/editor/refresh_displays [ at @s ]
#

# Run as the mystery box marker, at it.
data modify storage mgs:temp _ed_mb set value {yaw:0.0f,pitch:0.0f}
data modify storage mgs:temp _ed_mb.yaw set from entity @s data.yaw
data modify storage mgs:temp _ed_mb.pitch set from entity @s data.pitch
scoreboard players set @s mgs.mb.roll 0
execute if data entity @s data.roll store result score @s mgs.mb.roll run data get entity @s data.roll
scoreboard players operation @s mgs.mb.roll /= #90 mgs.data
scoreboard players operation @s mgs.mb.roll %= #4 mgs.data
function mgs:v5.3.0/maps/editor/displays/turn_mystery_box with storage mgs:temp _ed_mb

