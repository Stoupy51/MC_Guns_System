
#> mgs:v5.1.0/maps/editor/strip_light_fields/barricade
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.1.0/maps/editor/save_zb_object
#

data remove storage mgs:temp _light
data modify storage mgs:temp _light set from storage mgs:temp _save_zb.block_enabled
execute store success score #light_differs mgs.data run data modify storage mgs:temp _light set value {id:"minecraft:oak_fence_gate",properties:{open:"false"}}
execute if score #light_differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.block_enabled
data remove storage mgs:temp _light
data modify storage mgs:temp _light set from storage mgs:temp _save_zb.block_disabled
execute store success score #light_differs mgs.data run data modify storage mgs:temp _light set value {id:"minecraft:oak_fence_gate",properties:{open:"true"}}
execute if score #light_differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.block_disabled

