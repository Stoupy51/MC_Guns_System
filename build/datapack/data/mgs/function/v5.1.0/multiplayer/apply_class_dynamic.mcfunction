
#> mgs:v5.1.0/multiplayer/apply_class_dynamic
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/apply_class
#			mgs:v5.1.0/multiplayer/apply_custom_match
#

# Clear player inventory
clear @s

# Apply armor
item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={}]
item replace entity @s armor.feet with iron_boots[unbreakable={}]

# Knife in hotbar.0 for every loadout: it is not part of the class slot list because no class can
# choose it away. Weapons therefore start at hotbar.1 (primary) and hotbar.2 (secondary).
item replace entity @s hotbar.0 with minecraft:iron_sword[unbreakable={},custom_data={mgs:{knife:true}},item_name={"translate":"mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"},{type:"attack_speed",amount:-2.5,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_speed"},{type:"entity_interaction_range",amount:-1.0,operation:"add_value",slot:"mainhand",id:"mgs:knife_range"}]]

# Copy class slots to iteration temp
data modify storage mgs:temp slots set from storage mgs:temp current_class.slots

# Recursively apply all slots
execute if data storage mgs:temp slots[0] run function mgs:v5.1.0/multiplayer/apply_next_slot

# Apply perks from the selected loadout (standard class or custom)
function mgs:v5.1.0/multiplayer/apply_perks

# Give class menu item (only in multiplayer)
execute if entity @s[tag=mgs.give_class_menu] run loot replace entity @s hotbar.4 loot mgs:i/class_menu

