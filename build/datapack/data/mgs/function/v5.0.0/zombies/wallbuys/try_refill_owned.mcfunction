
#> mgs:v5.0.0/zombies/wallbuys/try_refill_owned
#
# @within	mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

execute if score #wb_purchase_done mgs.data matches 1 run return 0

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.1"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:1,inventory:1,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.2"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:2,inventory:2,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.3"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:3,inventory:3,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

