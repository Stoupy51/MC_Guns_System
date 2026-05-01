
#> mgs:v5.0.0/zombies/bonus/extract_mag_data
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"$(slot)"}
#
# @args		slot (string)
#

# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag=mgs.refilling_mag] $(slot)

# Special consumable compatibility (get max_stack_size, 64 by default)
execute store success score #is_consumable mgs.data if data entity @s item.components."minecraft:custom_data".mgs{consumable:1b}
execute if score #is_consumable mgs.data matches 1 run scoreboard players set #stack_size mgs.data 64
execute if score #is_consumable mgs.data matches 1 if data entity @s item.components."minecraft:max_stack_size" store result score #stack_size mgs.data run data get entity @s item.components."minecraft:max_stack_size"

# Read capacity and store as remaining_bullets (refill = set bullets to capacity)
execute store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
execute store result storage mgs:temp remaining_bullets int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity
execute store result storage mgs:temp capacity int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

# Store weapon name, slot, and current item_model for model update macro
data modify storage mgs:temp refill set value {}
$data modify storage mgs:temp refill.slot set value "$(slot)"
data modify storage mgs:temp refill.base_weapon set from entity @s item.components."minecraft:custom_data".mgs.weapon
data modify storage mgs:temp refill.mag_model set from entity @s item.components."minecraft:item_model"

# Clean up item_display
kill @s

