
#> mgs:v5.0.0/zombies/wallbuys/compute_effective_price
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/wallbuys/on_hover with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

scoreboard players set #wb_price_locked mgs.data 0
scoreboard players set #wb_price_mode mgs.data 0

# Slot 1 refill candidate
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:1,weapon_id:"$(weapon_id)"}
execute if score #wb_same_weapon mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.1"}
execute if score #wb_price_locked mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run return run function mgs:v5.0.0/zombies/wallbuys/select_refill_price {hotbar:1}

# Slot 2 refill candidate
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:2,weapon_id:"$(weapon_id)"}
execute if score #wb_same_weapon mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.2"}
execute if score #wb_price_locked mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run return run function mgs:v5.0.0/zombies/wallbuys/select_refill_price {hotbar:2}

# Slot 3 refill candidate
$function mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot {slot:3,weapon_id:"$(weapon_id)"}
execute if score #wb_same_weapon mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.3"}
execute if score #wb_price_locked mgs.data matches 0 if score #wb_same_weapon mgs.data matches 1 if score #wb_mag_not_full mgs.data matches 1 run return run function mgs:v5.0.0/zombies/wallbuys/select_refill_price {hotbar:3}

