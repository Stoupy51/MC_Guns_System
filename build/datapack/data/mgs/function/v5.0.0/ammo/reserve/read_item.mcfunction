
#> mgs:v5.0.0/ammo/reserve/read_item
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reserve/extract_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Copy item to entity
$item replace entity @s contents from entity @p[tag=mgs.reading_reserve] $(slot)

# Consumable: stack count = bullet count
execute if data entity @s item.components."minecraft:custom_data".mgs.consumable store result score #mag_bullets mgs.data run data get entity @s item.count

# Non-consumable: read remaining_bullets from custom data
execute unless data entity @s item.components."minecraft:custom_data".mgs.consumable store result score #mag_bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets

# Add to reserve
scoreboard players operation @p[tag=mgs.reading_reserve] mgs.reserve_ammo += #mag_bullets mgs.data

# Kill entity
kill @s

