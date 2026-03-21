
#> mgs:v5.0.0/zombies/wallbuys/process_purchase
#
# @within	mgs:v5.0.0/zombies/mystery_box/default_give/ak47 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m16a4 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/famas with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/aug with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m4a1 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/fnfal with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/g3a3 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/scar17 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mp5 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mp7 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mac10 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/ppsh41 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/sten with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m249 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/rpk with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/svd with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m82 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mosin with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m24 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/spas12 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m500 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m590 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/rpg7 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m1911 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m9 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/deagle with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/makarov with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/glock17 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/glock18 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/vz61 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#
# @args		weapon_id (string)
#			magazine_id (string)
#

scoreboard players set #wb_purchase_done mgs.data 0
scoreboard players set #wb_purchase_mode mgs.data 0

# Count guns in hotbar to determine placement logic
function mgs:v5.0.0/zombies/wallbuys/count_guns

# Always prioritize refill of the same weapon to prevent duplicates.
execute if score #wb_purchase_done mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/try_refill_owned with storage mgs:temp _wb_weapon

# New placement logic
$execute if score #wb_gun_count mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/give_to_slot {hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_gun_count mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/give_to_slot {hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_gun_count mgs.data matches 2 if score @s mgs.zb.perk.mule_kick matches 1.. run function mgs:v5.0.0/zombies/wallbuys/give_to_slot {hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}

# Otherwise replace the currently selected gun slot (1/2/3 only)
execute if score #wb_purchase_done mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/replace_selected with storage mgs:temp _wb_weapon

