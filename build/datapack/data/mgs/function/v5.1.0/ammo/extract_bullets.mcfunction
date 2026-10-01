
#> mgs:v5.1.0/ammo/extract_bullets
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/inventory/process_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.extracting_bullets] $(slot)

# A consumable (1b) counts one bullet per item; regular and converted magazines read remaining_bullets.
execute if data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #bullets mgs.data run data get entity @s item.count
execute unless data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets

execute store result storage mgs:temp capacity int 1 run data get entity @s item.components."minecraft:custom_data".mgs.stats.capacity

kill @s

