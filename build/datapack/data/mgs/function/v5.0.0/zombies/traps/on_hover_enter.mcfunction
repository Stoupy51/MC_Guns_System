
#> mgs:v5.0.0/zombies/traps/on_hover_enter
#
# @within	???
#

execute store result score #trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
title @s times 0 40 10
title @s title [[{"text":"⚠ ","color":"red"}, {"translate":"mgs.trap"}]]
title @s subtitle [{"translate":"mgs.cost_2","color":"gray"},{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]]

