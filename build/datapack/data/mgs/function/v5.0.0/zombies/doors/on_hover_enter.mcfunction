
#> mgs:v5.0.0/zombies/doors/on_hover_enter
#
# @within	???
#

execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price
title @s times 0 40 10
title @s title [{"text":"🚪 Door","color":"gold"}]
title @s subtitle [{"text":"Cost: ","color":"gray"},{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},{"text":" points","color":"gray"}]

