
#> mgs:v5.0.0/switch/do_toggle
#
# @executed	as @n[type=item,distance=..3,nbt={...}]
#
# @within	mgs:v5.0.0/switch/toggle_fire_mode [ as @n[type=item,distance=..3,nbt={...}] ]
#

# Get current fire mode
data modify storage mgs:temp fire_mode set from entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode

# Check weapon capabilities
execute store result score #has_auto mgs.data if data entity @s Item.components."minecraft:custom_data".mgs.stats.can_auto
execute store result score #has_burst mgs.data if data entity @s Item.components."minecraft:custom_data".mgs.stats.can_burst

# 3-way toggle for weapons with auto and burst: auto -> semi -> burst -> auto
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"auto"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "semi"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"semi"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "burst"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"burst"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "auto"

# 2-way toggle for weapons with auto but no burst: auto -> semi -> auto
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 0 if data storage mgs:temp {fire_mode:"auto"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "semi"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 0 if data storage mgs:temp {fire_mode:"semi"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "auto"

# 2-way toggle for weapons with burst but no auto: semi -> burst -> semi
execute if score #has_auto mgs.data matches 0 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"semi"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "burst"
execute if score #has_auto mgs.data matches 0 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"burst"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "semi"

# Weapons with neither auto nor burst stay on semi (should not happen)
# Default to auto if missing and weapon supports it, otherwise semi
execute unless data storage mgs:temp fire_mode if score #has_auto mgs.data matches 1 run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "auto"
execute unless data storage mgs:temp fire_mode if score #has_auto mgs.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "semi"

# Give item back to player's mainhand and kill the item entity
item replace entity @p weapon.mainhand from entity @s contents
kill @s

# Play feedback sound
playsound minecraft:block.note_block.hat ambient @p

