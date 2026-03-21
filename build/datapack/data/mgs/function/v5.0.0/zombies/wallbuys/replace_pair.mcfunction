
#> mgs:v5.0.0/zombies/wallbuys/replace_pair
#
# @within	mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
#
# @args		hotbar (int)
#			weapon_id (string)
#			inventory (int)
#			magazine_id (string)
#

$loot replace entity @s hotbar.$(hotbar) loot mgs:i/$(weapon_id)

scoreboard players set #wb_mag_given mgs.data 0
$execute store success score #wb_mag_given mgs.data run loot replace entity @s inventory.$(inventory) loot mgs:i/$(magazine_id)
$execute if score #wb_mag_given mgs.data matches 0 run item replace entity @s inventory.$(inventory) with air

$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
$execute if score #wb_mag_given mgs.data matches 1 run function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
$execute if score #wb_mag_given mgs.data matches 1 run function mgs:v5.0.0/zombies/inventory/scale_magazine_slot {slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}

$function mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"hotbar.$(hotbar)"}

scoreboard players set #wb_purchase_done mgs.data 1
scoreboard players set #wb_purchase_mode mgs.data 3

