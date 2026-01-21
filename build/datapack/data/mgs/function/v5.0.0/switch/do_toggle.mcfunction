
#> mgs:v5.0.0/switch/do_toggle
#
# @executed	as @n[type=item,distance=..3,nbt={...}]
#
# @within	mgs:v5.0.0/switch/toggle_fire_mode [ as @n[type=item,distance=..3,nbt={...}] ]
#

# Check if weapon supports burst fire, otherwise skip toggle
execute unless data entity @s Item.components."minecraft:custom_data".mgs.stats.can_burst run return fail

# Get current fire mode
data modify storage mgs:temp fire_mode set from entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode

# Toggle: auto -> burst, burst -> auto (default to burst if missing)
execute if data storage mgs:temp {fire_mode:"auto"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "burst"
execute if data storage mgs:temp {fire_mode:"burst"} run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "auto"
execute unless data storage mgs:temp fire_mode run data modify entity @s Item.components."minecraft:custom_data".mgs.stats.fire_mode set value "burst"

# Give item back to player's mainhand and kill the item entity
item replace entity @p weapon.mainhand from entity @s contents
kill @s

# Play feedback sound
playsound minecraft:block.note_block.hat ambient @p

