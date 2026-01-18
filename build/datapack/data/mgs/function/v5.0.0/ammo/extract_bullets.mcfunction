
#> mgs:v5.0.0/ammo/extract_bullets
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Copy item to entity
$item replace entity @s contents from entity @p[tag=mgs.extracting_bullets] $(slot)

# Get bullets
execute store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets

# Get magazine capacity
execute store result storage mgs:temp capacity int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

# Kill entity
kill @s

