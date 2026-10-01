
#> mgs:v5.1.0/zombies/wallbuys/on_right_click
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/setup_iter {run:"function mgs:v5.1.0/zombies/wallbuys/on_right_click",executor:"source"} [ as @n[tag=mgs.wb_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

# Read first: the dynamic price needs them.
execute store result storage mgs:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.1.0/zombies/wallbuys/lookup_weapon with storage mgs:temp _wb_buy
function mgs:v5.1.0/zombies/wallbuys/get_display_name

execute store result score #wb_buy_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
execute store result score #wb_rfprice mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfprice
execute store result score #wb_rfpap mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfpap

# Knife, lethal grenade and tactical have their own flows.
execute if data storage mgs:temp _wb_weapon{kind:1} run return run function mgs:v5.1.0/zombies/wallbuys/buy_knife with storage mgs:temp _wb_weapon
execute if data storage mgs:temp _wb_weapon{kind:2} run return run function mgs:v5.1.0/zombies/wallbuys/buy_lethal with storage mgs:temp _wb_weapon
execute if data storage mgs:temp _wb_weapon{kind:3} run return run function mgs:v5.1.0/zombies/wallbuys/buy_tactical with storage mgs:temp _wb_weapon

# Buy, refill or PaP refill.
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
function mgs:v5.1.0/zombies/wallbuys/compute_effective_price with storage mgs:temp _wb_weapon

execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#wb_price",obj:"mgs.data"}

scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data

function mgs:v5.1.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

execute if score #wb_purchase_mode mgs.data matches 1 run function mgs:v5.1.0/zombies/wallbuys/msg_purchased
execute if score #wb_purchase_mode mgs.data matches 2 run function mgs:v5.1.0/zombies/wallbuys/msg_refilled
execute if score #wb_purchase_mode mgs.data matches 3 run function mgs:v5.1.0/zombies/wallbuys/msg_replaced
execute if score #wb_purchase_mode mgs.data matches 4 run scoreboard players operation @s mgs.zb.points += #wb_price mgs.data
execute if score #wb_purchase_mode mgs.data matches 4 run function mgs:v5.1.0/zombies/wallbuys/msg_refund_full

# The actionbar reads reserve_ammo, which is otherwise only recomputed on reload, idle or weapon switch.
execute if score #wb_purchase_mode mgs.data matches 1..3 run function mgs:v5.1.0/utils/copy_gun_data
execute if score #wb_purchase_mode mgs.data matches 1..3 run function mgs:v5.1.0/ammo/compute_reserve

