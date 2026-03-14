
#> mgs:v5.0.0/zombies/inventory/give_ability_item
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout
#

item replace entity @s hotbar.4 with minecraft:paper[custom_data={mgs:{zb_ability_item:true}},consumable={consume_seconds:1000000,animation:"spear",sound:"minecraft:intentionally_empty",has_consume_particles:false},food={saturation:0,nutrition:0,can_always_eat:true},use_effects={can_sprint:true,speed_multiplier:1.0,interact_vibrations:false},item_name={"translate":"mgs.use_ability","color":"green","italic":false},lore=[{"translate":"mgs.right_click_to_activate","color":"gray","italic":false}]]
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.4",group:"hotbar",index:4}

