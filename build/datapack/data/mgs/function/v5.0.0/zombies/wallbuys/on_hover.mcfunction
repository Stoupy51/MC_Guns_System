
#> mgs:v5.0.0/zombies/wallbuys/on_hover
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup_iter {run:"function mgs:v5.0.0/zombies/wallbuys/on_hover",executor:"source"} [ as @n[tag=mgs.wb_new] ]
#

execute store result storage mgs:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.0.0/zombies/wallbuys/get_hover_name with storage mgs:temp _wb_hover
function mgs:v5.0.0/zombies/wallbuys/get_display_name

# Dynamic hover price (buy, refill, or PAP refill)
execute store result score #wb_buy_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
execute store result score #wb_rfprice mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfprice
execute store result score #wb_rfpap mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.rfpap
scoreboard players operation #wb_price mgs.data = #wb_buy_price mgs.data
function mgs:v5.0.0/zombies/wallbuys/compute_effective_price with storage mgs:temp _wb_weapon
function mgs:v5.0.0/zombies/wallbuys/set_hover_price_suffix

data modify storage smithed.actionbar:input message set value {json:[{"text":"🔫 ","color":"gold"},{"storage":"mgs:temp","nbt":"_wb_display_name","color":"yellow","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}],{"storage":"mgs:temp","nbt":"_wb_price_suffix","color":"gray","interpret":true}],priority:'notification',freeze:5}
function #smithed.actionbar:message

