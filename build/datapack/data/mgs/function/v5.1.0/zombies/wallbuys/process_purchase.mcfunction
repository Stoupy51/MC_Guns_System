
#> mgs:v5.1.0/zombies/wallbuys/process_purchase
#
# @within	mgs:v5.1.0/zombies/mystery_box/default_give/weapon with storage mgs:temp _wb_weapon
#			mgs:v5.1.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#			magazine_id (unknown)
#

scoreboard players set #wb_purchase_done mgs.data 0
scoreboard players set #wb_purchase_mode mgs.data 0

# Always prioritize refill of the same weapon to prevent duplicates.
execute if score #wb_purchase_done mgs.data matches 0 run function mgs:v5.1.0/zombies/wallbuys/try_refill_owned with storage mgs:temp _wb_weapon

# New placement: give to the first empty gun slot (checks each slot individually)
$execute if score #wb_purchase_done mgs.data matches 0 unless items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.1.0/zombies/wallbuys/give_to_slot {hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 unless items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.1.0/zombies/wallbuys/give_to_slot {hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 unless items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] if score @s mgs.zb.perk.mule_kick matches 1.. run function mgs:v5.1.0/zombies/wallbuys/give_to_slot {hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}

# Otherwise replace the currently selected gun slot (1/2/3 only)
execute if score #wb_purchase_done mgs.data matches 0 run function mgs:v5.1.0/zombies/wallbuys/replace_selected with storage mgs:temp _wb_weapon

