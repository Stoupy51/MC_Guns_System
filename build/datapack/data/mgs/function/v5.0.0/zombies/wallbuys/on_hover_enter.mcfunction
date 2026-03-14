
#> mgs:v5.0.0/zombies/wallbuys/on_hover_enter
#
# @within	???
#

execute store result score #wb_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
execute store result storage mgs:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.id
function mgs:v5.0.0/zombies/wallbuys/get_hover_name with storage mgs:temp _wb_hover
title @s times 0 40 10
title @s title [{"text":"🔫 ","color":"gold"},{"storage":"mgs:temp","nbt":"wb_hover_name","color":"gold"}]
title @s subtitle [{"translate":"mgs.cost_2","color":"gray"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]]

