
#> mgs:v5.0.0/zombies/wallbuys/try_refill_owned
#
# @within	mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#			magazine_id (unknown)
#

execute if score #wb_purchase_done mgs.data matches 1 run return 0

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.1"}
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:1,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.2"}
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:2,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.3"}
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:3,weapon_id:"$(weapon_id)"}
$execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/reload_pair {hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}
execute if score #wb_purchase_done mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 0 run function mgs:v5.0.0/zombies/wallbuys/refill_already_full

