
#> mgs:v5.1.0/ammo/reserve/read_item
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/reserve/extract_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

$item replace entity @s contents from entity @p[tag=mgs.reading_reserve] $(slot)

# A consumable (1b) counts one bullet per item.
execute if data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #mag_bullets mgs.data run data get entity @s item.count

# Others read remaining_bullets.
execute unless data entity @s item.components."minecraft:custom_data".mgs{consumable:1b} store result score #mag_bullets mgs.data run data get entity @s item.components."minecraft:custom_data".mgs.stats.remaining_bullets

scoreboard players operation @p[tag=mgs.reading_reserve] mgs.reserve_ammo += #mag_bullets mgs.data

kill @s

