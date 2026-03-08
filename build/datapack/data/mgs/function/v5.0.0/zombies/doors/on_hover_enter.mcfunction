
#> mgs:v5.0.0/zombies/doors/on_hover_enter
#
# @within	???
#

execute store result score #_door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price
title @s times 0 40 10
title @s title [{"text":"🚪 Door","color":"gold","bold":true}]
title @s subtitle [{"text":"Cost: ","color":"gray"},{"score":{"name":"#_door_price","objective":"mgs.data"},"color":"yellow"},{"translate": "mgs.points","color":"gray"}]

