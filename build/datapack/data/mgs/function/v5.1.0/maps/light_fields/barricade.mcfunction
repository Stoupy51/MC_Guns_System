
#> mgs:v5.1.0/maps/light_fields/barricade
#
# @executed	as @n[tag=mgs._barricade_new_d]
#
# @within	mgs:v5.1.0/zombies/barricades/setup_iter [ as @n[tag=mgs._barricade_new_d] ]
#			mgs:v5.1.0/maps/editor/backfill_zb_defaults
#

# @s = an entity holding one saved barricade compound in data (editor marker or in-game display)
execute if data entity @s data.block_enabled.Name run data modify entity @s data.block_enabled.id set from entity @s data.block_enabled.Name
execute if data entity @s data.block_enabled.Properties run data modify entity @s data.block_enabled.properties set from entity @s data.block_enabled.Properties
data remove entity @s data.block_enabled.Name
data remove entity @s data.block_enabled.Properties
execute unless data entity @s data.block_enabled run data modify entity @s data.block_enabled set value {id:"minecraft:oak_fence_gate",properties:{open:"false"}}
execute if data entity @s data.block_disabled.Name run data modify entity @s data.block_disabled.id set from entity @s data.block_disabled.Name
execute if data entity @s data.block_disabled.Properties run data modify entity @s data.block_disabled.properties set from entity @s data.block_disabled.Properties
data remove entity @s data.block_disabled.Name
data remove entity @s data.block_disabled.Properties
execute unless data entity @s data.block_disabled run data modify entity @s data.block_disabled set value {id:"minecraft:oak_fence_gate",properties:{open:"true"}}

