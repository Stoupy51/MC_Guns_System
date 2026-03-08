
#> mgs:v5.0.0/zombies/perks/on_hover_enter
#
# @within	???
#

execute store result score #pk_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.price
title @s times 0 40 10
title @s title [{"translate": "mgs.perk_machine","color":"dark_purple"}]
title @s subtitle [{"translate": "mgs.cost","color":"gray"},{"score":{"name":"#pk_price","objective":"mgs.data"},"color":"yellow"},{"translate": "mgs.points","color":"gray"}]

