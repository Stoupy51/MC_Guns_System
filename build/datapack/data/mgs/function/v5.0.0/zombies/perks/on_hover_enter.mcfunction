
#> mgs:v5.0.0/zombies/perks/on_hover_enter
#
# @within	???
#

execute store result score #_pk_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.price
title @s times 0 40 10
title @s title [{"text":"🥤 Perk Machine","color":"dark_purple","bold":true}]
title @s subtitle [{"text":"Cost: ","color":"gray"},{"score":{"name":"#_pk_price","objective":"mgs.data"},"color":"yellow"},{"translate": "mgs.points","color":"gray"}]

