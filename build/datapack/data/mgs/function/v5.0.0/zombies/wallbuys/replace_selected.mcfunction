
#> mgs:v5.0.0/zombies/wallbuys/replace_selected
#
# @within	mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

scoreboard players set #wb_valid_sel mgs.data 0
execute store result score #wb_sel mgs.data run data get entity @s SelectedItemSlot

$execute if score #wb_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.1"}
$execute if score #wb_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}
$execute if score #wb_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.0.0/zombies/wallbuys/replace_pair {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}

$execute if score #wb_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.2"}
$execute if score #wb_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}
$execute if score #wb_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.0.0/zombies/wallbuys/replace_pair {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}

$execute if score #wb_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.3"}
$execute if score #wb_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}
$execute if score #wb_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run function mgs:v5.0.0/zombies/wallbuys/replace_pair {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}

execute if score #wb_purchase_done mgs.data matches 0 run scoreboard players operation @s mgs.zb.points += #wb_price mgs.data
execute if score #wb_purchase_done mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/deny_hold_valid_slot
execute if score #wb_purchase_done mgs.data matches 0 run scoreboard players set #wb_purchase_mode mgs.data -1

