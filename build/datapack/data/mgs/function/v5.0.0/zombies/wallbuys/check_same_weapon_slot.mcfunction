
#> mgs:v5.0.0/zombies/wallbuys/check_same_weapon_slot
#
# @within	mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:1,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:2,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:3,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:1,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:2,weapon_id:"$(weapon_id)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:3,weapon_id:"$(weapon_id)"}
#
# @args		slot (int)
#			weapon_id (string)
#

scoreboard players set #wb_same_weapon mgs.data 0
$execute store success score #wb_same_weapon mgs.data run data get entity @s Inventory[{Slot:$(slot)b}].components."minecraft:custom_data".mgs.$(weapon_id)

