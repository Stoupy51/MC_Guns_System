
#> mgs:v5.1.0/multiplayer/drop_capture_mag
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/drop_held_weapon with storage mgs:temp _dropmag_args
#
# @args		mag (unknown)
#			halfc (unknown)
#

summon minecraft:item_display ~ ~ ~ {Tags:["mgs.mp_mag_helper"]}
$loot replace entity @n[tag=mgs.mp_mag_helper] contents loot mgs:i/$(mag)
data modify storage mgs:temp _dropmag set from entity @n[tag=mgs.mp_mag_helper] item
kill @n[tag=mgs.mp_mag_helper]
execute unless data storage mgs:temp _dropmag run return 0

# Regular magazines: fill to 50% of their capacity (never a full magazine)
execute store result score #mag_half mgs.data run data get storage mgs:temp _dropmag.components."minecraft:custom_data".mgs.stats.capacity
scoreboard players operation #mag_half mgs.data /= #2 mgs.data
execute if score #mag_half mgs.data matches ..0 run scoreboard players set #mag_half mgs.data 1
execute unless data storage mgs:temp _dropmag.components."minecraft:custom_data".mgs.consumable store result storage mgs:temp _dropmag.components."minecraft:custom_data".mgs.stats.remaining_bullets int 1 run scoreboard players get #mag_half mgs.data

# Consumable ammo (stack count = bullets): half of one full stack
$execute if data storage mgs:temp _dropmag.components."minecraft:custom_data".mgs.consumable run data modify storage mgs:temp _dropmag.count set value $(halfc)

