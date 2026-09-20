
#> mgs:v5.1.0/zombies/wallbuys/refill_lethal
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/buy_lethal with storage mgs:temp _wb_weapon
#			mgs:v5.1.0/zombies/wallbuys/buy_lethal_web with storage mgs:temp _wb_weapon
#

# Already at max: deny without charging (no points were deducted yet on this path)
execute store result score #wb_eq_count mgs.data run data get entity @s Inventory[{Slot:7b}].count
execute if score #wb_eq_count mgs.data matches 4.. run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.your_equipment_is_already_full","color":"yellow"}'}

# Refill price
scoreboard players operation #wb_price mgs.data = #wb_rfprice mgs.data
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#wb_price",obj:"mgs.data"}
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
function mgs:v5.1.0/zombies/wallbuys/msg_refilled

