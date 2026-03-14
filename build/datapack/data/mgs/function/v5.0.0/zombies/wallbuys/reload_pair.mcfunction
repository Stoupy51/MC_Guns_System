
#> mgs:v5.0.0/zombies/wallbuys/reload_pair
#
# @within	mgs:v5.0.0/zombies/wallbuys/try_refill_owned {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}
#
# @args		inventory (int)
#			weapon_id (unknown)
#			hotbar (int)
#

scoreboard players set #wb_new_mag mgs.data 0
$execute unless items entity @s inventory.$(inventory) *[custom_data~{mgs:{magazine:true}}] run scoreboard players set #wb_new_mag mgs.data 1
$execute if score #wb_new_mag mgs.data matches 1 run loot replace entity @s inventory.$(inventory) loot mgs:i/$(weapon_id)_mag
$execute if score #wb_new_mag mgs.data matches 1 run function mgs:v5.0.0/zombies/inventory/scale_magazine_slot {slot:"inventory.$(inventory)"}

$function mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"hotbar.$(hotbar)"}
$function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.$(inventory)"}

$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}

scoreboard players set #wb_purchase_done mgs.data 1
scoreboard players set #wb_purchase_mode mgs.data 2

