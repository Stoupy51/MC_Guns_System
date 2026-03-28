
#> mgs:v5.0.0/zombies/wallbuys/on_right_click
#
# @within	???
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Get wallbuy id + data first (used by dynamic price logic)
execute store result storage mgs:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.0.0/zombies/wallbuys/lookup_weapon with storage mgs:temp _wb_buy
function mgs:v5.0.0/zombies/wallbuys/get_display_name

# Read all possible prices from wallbuy entity
execute store result score #wb_buy_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
execute store result score #wb_rfprice mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfprice
execute store result score #wb_rfpap mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfpap

# Compute effective price for this interaction (buy vs refill vs PAP refill)
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
function mgs:v5.0.0/zombies/wallbuys/compute_effective_price with storage mgs:temp _wb_weapon

# Check player has enough points
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run function mgs:v5.0.0/zombies/wallbuys/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data

# Process buy by zombies inventory rules
function mgs:v5.0.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon

execute if score #wb_purchase_mode mgs.data matches 1 run function mgs:v5.0.0/zombies/wallbuys/msg_purchased
execute if score #wb_purchase_mode mgs.data matches 2 run function mgs:v5.0.0/zombies/wallbuys/msg_refilled
execute if score #wb_purchase_mode mgs.data matches 3 run function mgs:v5.0.0/zombies/wallbuys/msg_replaced
execute if score #wb_purchase_mode mgs.data matches 4 run scoreboard players operation @s mgs.zb.points += #wb_price mgs.data
execute if score #wb_purchase_mode mgs.data matches 4 run function mgs:v5.0.0/zombies/wallbuys/msg_refund_full

