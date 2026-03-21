
#> mgs:v5.0.0/zombies/wallbuys/check_mag_not_full
#
# @within	mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:"inventory.2"}
#			mgs:v5.0.0/zombies/wallbuys/try_refill_owned {slot:"inventory.3"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:"inventory.2"}
#			mgs:v5.0.0/zombies/wallbuys/replace_selected {slot:"inventory.3"}
#
# @args		slot (string)
#

scoreboard players set #wb_mag_not_full mgs.data 0

# Missing paired mag counts as not full.
$execute unless items entity @s $(slot) *[custom_data~{mgs:{magazine:true}}] run scoreboard players set #wb_mag_not_full mgs.data 1

tag @s add mgs.wb_reading_mag
$execute if items entity @s $(slot) *[custom_data~{mgs:{magazine:true}}] summon minecraft:item_display run function mgs:v5.0.0/zombies/wallbuys/read_mag_state {slot:"$(slot)"}
tag @s remove mgs.wb_reading_mag

execute if score #wb_mag_rem mgs.data < #wb_mag_cap mgs.data run scoreboard players set #wb_mag_not_full mgs.data 1

