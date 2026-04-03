
#> mgs:v5.0.0/zombies/doors/on_hover
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.0.0/zombies/doors/setup_iter {run:"function mgs:v5.0.0/zombies/doors/on_hover",executor:"source"} [ as @e[tag=mgs.door_new] ]
#

execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price
execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link
execute store result storage mgs:temp _door_hover.id int 1 run scoreboard players get #door_link mgs.data
execute if entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.0.0/zombies/doors/get_hover_name_back with storage mgs:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.0.0/zombies/doors/get_hover_name with storage mgs:temp _door_hover
data modify storage smithed.actionbar:input message set value {json:[{"text":"🛠 ","color":"gold"},{"storage":"mgs:temp","nbt":"_door_hover_name","color":"yellow","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

