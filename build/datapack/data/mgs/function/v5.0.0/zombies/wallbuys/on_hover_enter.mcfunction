
#> mgs:v5.0.0/zombies/wallbuys/on_hover_enter
#
# @within	???
#

execute store result score #wb_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wb.price
title @s times 0 40 10
title @s title [{"text":"🔫 Wallbuy","color":"gold"}]
title @s subtitle [{"text":"Cost: ","color":"gray"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},{"text":" points","color":"gray"}]

