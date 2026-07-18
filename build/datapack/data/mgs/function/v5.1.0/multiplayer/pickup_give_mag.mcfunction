
#> mgs:v5.1.0/multiplayer/pickup_give_mag
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_collect
#

data modify storage mgs:temp _give set value {}
data modify storage mgs:temp _give.Item set from entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag
data modify storage mgs:temp _give.Owner set from entity @s UUID

# Load the magazine into a helper display so `item replace ... from entity` can read it
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.mp_mag_helper"]}
data modify entity @n[tag=mgs.mp_mag_helper] item set from storage mgs:temp _give.Item

# First free main-inventory slot
scoreboard players set #mag_slot mgs.data -1
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.0 * run scoreboard players set #mag_slot mgs.data 0
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.1 * run scoreboard players set #mag_slot mgs.data 1
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.2 * run scoreboard players set #mag_slot mgs.data 2
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.3 * run scoreboard players set #mag_slot mgs.data 3
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.4 * run scoreboard players set #mag_slot mgs.data 4
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.5 * run scoreboard players set #mag_slot mgs.data 5
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.6 * run scoreboard players set #mag_slot mgs.data 6
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.7 * run scoreboard players set #mag_slot mgs.data 7
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.8 * run scoreboard players set #mag_slot mgs.data 8
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.9 * run scoreboard players set #mag_slot mgs.data 9
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.10 * run scoreboard players set #mag_slot mgs.data 10
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.11 * run scoreboard players set #mag_slot mgs.data 11
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.12 * run scoreboard players set #mag_slot mgs.data 12
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.13 * run scoreboard players set #mag_slot mgs.data 13
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.14 * run scoreboard players set #mag_slot mgs.data 14
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.15 * run scoreboard players set #mag_slot mgs.data 15
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.16 * run scoreboard players set #mag_slot mgs.data 16
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.17 * run scoreboard players set #mag_slot mgs.data 17
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.18 * run scoreboard players set #mag_slot mgs.data 18
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.19 * run scoreboard players set #mag_slot mgs.data 19
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.20 * run scoreboard players set #mag_slot mgs.data 20
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.21 * run scoreboard players set #mag_slot mgs.data 21
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.22 * run scoreboard players set #mag_slot mgs.data 22
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.23 * run scoreboard players set #mag_slot mgs.data 23
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.24 * run scoreboard players set #mag_slot mgs.data 24
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.25 * run scoreboard players set #mag_slot mgs.data 25
execute if score #mag_slot mgs.data matches -1 unless items entity @s inventory.26 * run scoreboard players set #mag_slot mgs.data 26
execute store result storage mgs:temp _give.slot int 1 run scoreboard players get #mag_slot mgs.data
execute if score #mag_slot mgs.data matches 0.. run function mgs:v5.1.0/multiplayer/pickup_place_mag with storage mgs:temp _give

# Main inventory full -> fall back to an owner-locked ground item (may land in the hotbar)
execute if score #mag_slot mgs.data matches -1 at @s run function mgs:v5.1.0/multiplayer/pickup_give with storage mgs:temp _give

kill @n[tag=mgs.mp_mag_helper]
data remove entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag

