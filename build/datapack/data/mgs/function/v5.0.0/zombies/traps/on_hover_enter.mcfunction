
#> mgs:v5.0.0/zombies/traps/on_hover_enter
#
# @within	???
#

execute store result score #_trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
title @s times 0 40 10
title @s title [{"text":"⚠ Trap","color":"red","bold":true}]
title @s subtitle [{"text":"Cost: ","color":"gray"},{"score":{"name":"#_trap_price","objective":"mgs.data"},"color":"yellow"},{"translate": "mgs.points","color":"gray"}]

