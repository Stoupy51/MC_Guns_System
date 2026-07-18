
#> mgs:v5.1.0/maps/editor/displays/barrier
#
# @executed	as @e[tag=mgs.element.barrier] & at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[tag=mgs.element.barrier] & at @s ]
#

# @s = barrier marker, at @s
data modify storage mgs:temp _ed_bar.yaw set value 0.0f
execute if data entity @s data.yaw run data modify storage mgs:temp _ed_bar.yaw set from entity @s data.yaw

# Fall back to the element default when the marker has no block configured yet
data modify storage mgs:temp _ed_bar.block set value {Name:"minecraft:oak_fence_gate",Properties:{open:"false"}}
execute if data entity @s data.block_enabled run data modify storage mgs:temp _ed_bar.block set from entity @s data.block_enabled

execute align xyz positioned ~.5 ~.5 ~.5 run function mgs:v5.1.0/maps/editor/displays/summon_barrier with storage mgs:temp _ed_bar

