
#> mgs:v5.1.0/zombies/doors/on_right_click
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.1.0/zombies/doors/setup_iter {run:"function mgs:v5.1.0/zombies/doors/on_right_click",executor:"source"} [ as @e[tag=mgs.door_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

function mgs:v5.1.0/zombies/doors/read_price

execute unless score @s mgs.zb.points >= #door_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#door_price",obj:"mgs.data"}

scoreboard players operation @s mgs.zb.points -= #door_price mgs.data

execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link

# Front or back name, for the announce.
execute store result storage mgs:temp _door_hover.id int 1 run scoreboard players get #door_link mgs.data
execute if entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name_back with storage mgs:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name with storage mgs:temp _door_hover

# Chip-in progress is global: mirror it on every entity of the link group (both sides of every linked door).
scoreboard players operation #door_paid mgs.data += #door_price mgs.data
execute if score #door_partial mgs.data matches 1.. as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data run scoreboard players operation @s mgs.zb.door.paid = #door_paid mgs.data
execute if score #door_partial mgs.data matches 1.. if score #door_paid mgs.data < #door_total mgs.data run return run function mgs:v5.1.0/zombies/doors/announce_progress

execute as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data at @s run function mgs:v5.1.0/zombies/doors/open_one

# Announces the total, not the last chunk.
tag @a remove mgs.xp_earner
tag @s add mgs.xp_earner
tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"green"}, {"translate":"mgs.opened"}],{"storage":"mgs:temp","nbt":"_door_hover_name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for"}],{"score":{"name":"#door_total","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3"}]]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}],[{"text":" ","color":"green"}, {"translate":"mgs.opened"}],{"storage":"mgs:temp","nbt":"_door_hover_name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for"}],{"score":{"name":"#door_total","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3"}],[" ",{"text":"+3 XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/zb/award_door
tag @a remove mgs.xp_earner
playsound minecraft:block.note_block.bit ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 0.9

