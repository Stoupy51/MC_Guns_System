
#> mgs:v5.1.0/zombies/inventory/give_starting_loadout
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/preload_complete [ at @s ]
#			mgs:v5.1.0/zombies/join_game
#			mgs:v5.1.0/zombies/inventory/give_respawn_loadout
#

clear @s

item replace entity @s hotbar.0 with minecraft:iron_sword[unbreakable={},custom_data={mgs:{knife:true,combat_knife:true}},item_model="mgs:combat_knife",item_name={"translate":"mgs.knife","color":"white","italic":false},attribute_modifiers=[{type:"movement_speed",amount: 0.1,operation:"add_multiplied_base",slot:"mainhand",id:"minecraft:base_movement_speed"},{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"},{type:"attack_speed",amount:-2.5,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_speed"}]]
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.0",group:"hotbar",index:0}

# Starting weapon and its scaled magazine.
loot replace entity @s hotbar.1 loot mgs:i/m1911
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.1",group:"hotbar",index:1}

loot replace entity @s inventory.1 loot mgs:i/m1911_mag
function mgs:v5.1.0/zombies/inventory/scale_magazine_slot {slot:"inventory.1",index:1,remaining_multiplier:0.5}
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"inventory.1",group:"inventory",index:1}

# Main equipment (frag); the lethal type is recorded so an empty slot refills with frag, not a stale value.
loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}
scoreboard players set @s mgs.zb.lethal_type 0

function mgs:v5.1.0/zombies/inventory/refresh_info_item

# Only for manual abilities.
execute if score @s mgs.zb.ability matches 3.. run function mgs:v5.1.0/zombies/inventory/give_ability_item

