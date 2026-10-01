
#> mgs:v5.1.0/maps/editor/displays/barricade
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ at @s ]
#

# Run as the barricade marker, at it.
data modify storage mgs:temp _ed_bar.yaw set value 0.0f
execute if data entity @s data.yaw run data modify storage mgs:temp _ed_bar.yaw set from entity @s data.yaw

# No block configured yet: the element default.
data modify storage mgs:temp _ed_bar.block set value {id:"minecraft:oak_fence_gate",properties:{open:"false"}}
execute if data entity @s data.block_enabled run data modify storage mgs:temp _ed_bar.block set from entity @s data.block_enabled

execute align xyz positioned ~.5 ~.5 ~.5 run function mgs:v5.1.0/maps/editor/displays/summon_barricade with storage mgs:temp _ed_bar

