
#> mgs:v5.0.0/ammo/extract_bullets
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Copy item to entity
$item replace entity @s contents from entity @p[tag=mgs.extracting_bullets] $(slot)

# For consumable magazines (1b = true consumable), the stack count IS the bullet count (each item = 1 bullet)
# For regular/converted magazines, read remaining_bullets from custom data
execute if data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #bullets mgs.data run data get entity @s item.count
execute unless data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets

# Get magazine capacity
execute store result storage mgs:temp capacity int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

# Kill entity
kill @s

