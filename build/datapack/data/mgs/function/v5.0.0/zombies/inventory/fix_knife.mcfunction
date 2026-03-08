
#> mgs:v5.0.0/zombies/inventory/fix_knife
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots
#

# Re-give any knife from wrong slots
clear @s minecraft:iron_sword[custom_data~{mgs:{knife:true}}]
item replace entity @s hotbar.0 with minecraft:iron_sword[custom_data={mgs:{knife:true}},item_name={"translate": "mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}]]

