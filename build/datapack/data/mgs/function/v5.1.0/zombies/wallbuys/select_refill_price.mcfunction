
#> mgs:v5.1.0/zombies/wallbuys/select_refill_price
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/compute_effective_price {hotbar:1,inventory:1}
#			mgs:v5.1.0/zombies/wallbuys/compute_effective_price {hotbar:2,inventory:2}
#			mgs:v5.1.0/zombies/wallbuys/compute_effective_price {hotbar:3,inventory:3}
#
# @args		hotbar (int)
#			inventory (int)
#

scoreboard players operation #wb_price mgs.data = #wb_rfprice mgs.data
scoreboard players set #wb_price_mode mgs.data 1

# PaP refill price when pap_level > 0.
scoreboard players set #wb_pap_level mgs.data 0
$execute store result score #wb_pap_level mgs.data run data get entity @s Inventory[{Slot:$(hotbar)b}].components."minecraft:custom_data".mgs.stats.pap_level
execute if score #wb_pap_level mgs.data matches 1.. run scoreboard players operation #wb_price mgs.data = #wb_rfpap mgs.data
execute if score #wb_pap_level mgs.data matches 1.. run scoreboard players set #wb_price_mode mgs.data 2

# Nothing to top up: the hover says so rather than charging and refunding.
$function mgs:v5.1.0/zombies/wallbuys/check_mag_not_full {slot:"inventory.$(inventory)"}
execute if score #wb_mag_not_full mgs.data matches 0 run scoreboard players set #wb_price_mode mgs.data 3

