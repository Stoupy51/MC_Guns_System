
#> mgs:v5.0.0/zombies/inventory/give_starting_loadout
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/preload_complete [ at @s ]
#			mgs:v5.0.0/zombies/inventory/give_respawn_loadout
#

# Clear existing inventory
clear @s

# hotbar.0: Knife
item replace entity @s hotbar.0 with minecraft:iron_sword[custom_data={mgs:{knife:true}},item_name={"translate":"mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}]]

# hotbar.1: Starting weapon (M1911)
loot replace entity @s hotbar.1 loot mgs:i/m1911

# inventory.1: M1911 magazine (dynamically scaled: base capacity * 8, half filled)
loot replace entity @s inventory.1 loot mgs:i/m1911_mag
execute store result score #zb_cap mgs.data run data get entity @s Inventory[{Slot:10b}].components."minecraft:custom_data".mgs.stats.capacity
scoreboard players set #zb_const mgs.data 8
scoreboard players operation #zb_cap mgs.data *= #zb_const mgs.data
execute store result storage mgs:temp zb_item_stats.capacity int 1 run scoreboard players get #zb_cap mgs.data
scoreboard players set #zb_const mgs.data 2
scoreboard players operation #zb_cap mgs.data /= #zb_const mgs.data
execute store result storage mgs:temp zb_item_stats.remaining_bullets int 1 run scoreboard players get #zb_cap mgs.data
item modify entity @s inventory.1 mgs:v5.0.0/zb_item_stats

# hotbar.7: Frag grenade (4 uses)
data modify storage mgs:temp zb_item_stats set value {capacity:4,remaining_bullets:4}
loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
item modify entity @s hotbar.7 mgs:v5.0.0/zb_item_stats

# hotbar.8: Player info item
function mgs:v5.0.0/zombies/inventory/refresh_info_item

# hotbar.4: Ability item (if ability is set)
execute if score @s mgs.zb.ability matches 1.. run function mgs:v5.0.0/zombies/inventory/give_ability_item

