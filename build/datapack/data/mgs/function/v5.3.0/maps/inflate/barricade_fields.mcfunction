
#> mgs:v5.3.0/maps/inflate/barricade_fields
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/inflate/barricade
#

function mgs:v5.3.0/maps/inflate/rotation
execute if data storage mgs:temp _inf.block_enabled.Name run data modify storage mgs:temp _inf.block_enabled.id set from storage mgs:temp _inf.block_enabled.Name
execute if data storage mgs:temp _inf.block_enabled.Properties run data modify storage mgs:temp _inf.block_enabled.properties set from storage mgs:temp _inf.block_enabled.Properties
data remove storage mgs:temp _inf.block_enabled.Name
data remove storage mgs:temp _inf.block_enabled.Properties
execute unless data storage mgs:temp _inf.block_enabled run data modify storage mgs:temp _inf.block_enabled set from storage mgs:temp _inf_shared.barricade.block_enabled
execute if data storage mgs:temp _inf.block_disabled.Name run data modify storage mgs:temp _inf.block_disabled.id set from storage mgs:temp _inf.block_disabled.Name
execute if data storage mgs:temp _inf.block_disabled.Properties run data modify storage mgs:temp _inf.block_disabled.properties set from storage mgs:temp _inf.block_disabled.Properties
data remove storage mgs:temp _inf.block_disabled.Name
data remove storage mgs:temp _inf.block_disabled.Properties
execute unless data storage mgs:temp _inf.block_disabled run data modify storage mgs:temp _inf.block_disabled set from storage mgs:temp _inf_shared.barricade.block_disabled
execute unless data storage mgs:temp _inf.block_enabled run data modify storage mgs:temp _inf.block_enabled set value {id:"minecraft:oak_fence_gate",properties:{open:"false"}}
execute unless data storage mgs:temp _inf.block_disabled run data modify storage mgs:temp _inf.block_disabled set value {id:"minecraft:oak_fence_gate",properties:{open:"true"}}
execute unless data storage mgs:temp _inf.radius run data modify storage mgs:temp _inf.radius set value 2

