
#> mgs:v5.0.0/zombies/doors/on_hover_enter
#
# @within	???
#

execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price
execute store result storage mgs:temp _door_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link
function mgs:v5.0.0/zombies/doors/get_hover_name with storage mgs:temp _door_hover
title @s times 0 40 10
title @s title [{"text":"🚪 ","color":"gold"},{"storage":"mgs:temp","nbt":"_door_hover_name","color":"gold"}]
title @s subtitle [{"translate":"mgs.cost_2","color":"gray"},{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]]

