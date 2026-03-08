
#> mgs:v5.0.0/zombies/wallbuys/on_right_click
#
# @within	???
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Get wallbuy price
execute store result score #wb_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price

# Check player has enough points
execute unless score @s mgs.zb.points >= #wb_price mgs.data run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points","color":"red"}]

# Deduct points
scoreboard players operation @s mgs.zb.points -= #wb_price mgs.data

# Get weapon_id from storage via wallbuy ID
execute store result storage mgs:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.0.0/zombies/wallbuys/lookup_weapon with storage mgs:temp _wb_buy

# Give weapon to player
function mgs:v5.0.0/zombies/wallbuys/give_weapon with storage mgs:temp _wb_weapon

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.weapon_purchased","color":"green"}]

