
#> mgs:v5.0.0/zombies/inventory/give_starting_loadout
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/preload_complete [ at @s ]
#			mgs:v5.0.0/zombies/inventory/give_respawn_loadout
#

clear @s

# hotbar.0: knife
item replace entity @s hotbar.0 with minecraft:iron_sword[unbreakable={},custom_data={mgs:{knife:true}},item_name={"translate":"mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}]]
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.0",group:"hotbar",index:0}

# hotbar.1 + inventory.1: starting weapon and scaled magazine
loot replace entity @s hotbar.1 loot mgs:i/m1911
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.1",group:"hotbar",index:1}

loot replace entity @s inventory.1 loot mgs:i/m1911_mag
function mgs:v5.0.0/zombies/inventory/scale_magazine_slot {slot:"inventory.1"}
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"inventory.1",group:"inventory",index:1}

# hotbar.7: main equipment (frag by default)
data modify storage mgs:temp zb_item_stats set value {capacity:4,remaining_bullets:4}
loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
item modify entity @s hotbar.7 mgs:v5.0.0/zb_item_stats
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

# hotbar.8: info item
function mgs:v5.0.0/zombies/inventory/refresh_info_item

# hotbar.4: only for manual abilities (automatic abilities must not show this item)
execute if score @s mgs.zb.ability matches 3.. run function mgs:v5.0.0/zombies/inventory/give_ability_item

