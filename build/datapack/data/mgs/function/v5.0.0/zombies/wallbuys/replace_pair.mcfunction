
#> mgs:v5.0.0/zombies/wallbuys/replace_pair
#
# @within	mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}
#
# @args		hotbar (int)
#			weapon_id (unknown)
#			inventory (int)
#

$loot replace entity @s hotbar.$(hotbar) loot mgs:i/$(weapon_id)
$loot replace entity @s inventory.$(inventory) loot mgs:i/$(weapon_id)_mag

$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}
$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}

$function mgs:v5.0.0/zombies/inventory/scale_magazine_slot {slot:"inventory.$(inventory)"}

$function mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"hotbar.$(hotbar)"}

scoreboard players set #wb_purchase_done mgs.data 1
scoreboard players set #wb_purchase_mode mgs.data 3

