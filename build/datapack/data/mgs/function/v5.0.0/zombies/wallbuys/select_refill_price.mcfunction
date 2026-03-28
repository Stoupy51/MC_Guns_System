
#> mgs:v5.0.0/zombies/wallbuys/select_refill_price
#
# @within	mgs:v5.0.0/zombies/wallbuys/compute_effective_price {hotbar:1}
#			mgs:v5.0.0/zombies/wallbuys/compute_effective_price {hotbar:2}
#			mgs:v5.0.0/zombies/wallbuys/compute_effective_price {hotbar:3}
#
# @args		hotbar (int)
#

# Default refill price
scoreboard players operation #wb_price mgs.data = #wb_rfprice mgs.data
scoreboard players set #wb_price_mode mgs.data 1

# PAP refill price if weapon in this slot has pap_level > 0
scoreboard players set #wb_pap_level mgs.data 0
$execute store result score #wb_pap_level mgs.data run data get entity @s Inventory[{Slot:$(hotbar)b}].components."minecraft:custom_data".mgs.stats.pap_level
execute if score #wb_pap_level mgs.data matches 1.. run scoreboard players operation #wb_price mgs.data = #wb_rfpap mgs.data
execute if score #wb_pap_level mgs.data matches 1.. run scoreboard players set #wb_price_mode mgs.data 2

scoreboard players set #wb_price_locked mgs.data 1

