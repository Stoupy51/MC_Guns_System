
#> mgs:v5.0.0/zombies/wallbuys/on_hover
#
# @within	???
#

execute store result score #wb_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
execute store result storage mgs:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.0.0/zombies/wallbuys/get_hover_name with storage mgs:temp _wb_hover
data modify storage smithed.actionbar:input message set value {json:[[{"text":"🔫 ","color":"gold"}, {"translate":"mgs.wallbuy"}],[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

