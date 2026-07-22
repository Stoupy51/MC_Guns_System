
#> mgs:v5.1.0/zombies/doors/on_hover
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.1.0/zombies/doors/setup_iter {run:"function mgs:v5.1.0/zombies/doors/on_hover",executor:"source"} [ as @e[tag=mgs.door_new] ]
#

function mgs:v5.1.0/zombies/doors/read_price
execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link
execute store result storage mgs:temp _door_hover.id int 1 run scoreboard players get #door_link mgs.data
execute if entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name_back with storage mgs:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name with storage mgs:temp _door_hover
execute unless score #door_partial mgs.data matches 1.. run data modify storage smithed.actionbar:input message set value {json:[{"text":"🛠 ","color":"gold"},{"storage":"mgs:temp","nbt":"_door_hover_name","color":"yellow","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:"conditional",freeze:5}
execute if score #door_partial mgs.data matches 1.. run data modify storage smithed.actionbar:input message set value {json:[{"text":"🛠 ","color":"gold"},{"storage":"mgs:temp","nbt":"_door_hover_name","color":"yellow","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.chip_in"}],{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}, "  ("],{"score":{"name":"#door_paid","objective":"mgs.data"},"color":"green"},{"text":"/","color":"gray"},{"score":{"name":"#door_total","objective":"mgs.data"},"color":"yellow"},{"text":")","color":"gray"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

