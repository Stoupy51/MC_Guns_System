
#> mgs:v5.1.0/zombies/doors/on_right_click
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.1.0/zombies/doors/setup_iter {run:"function mgs:v5.1.0/zombies/doors/on_right_click",executor:"source"} [ as @e[tag=mgs.door_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Get door price from interacted entity
function mgs:v5.1.0/zombies/doors/read_price

# Check player has enough points
execute unless score @s mgs.zb.points >= #door_price mgs.data run return run function mgs:v5.1.0/zombies/doors/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #door_price mgs.data

# Get link_id from interacted door
execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link

# Resolve door display name for announcement (front/back aware)
execute store result storage mgs:temp _door_hover.id int 1 run scoreboard players get #door_link mgs.data
execute if entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name_back with storage mgs:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag=mgs.door_back] run function mgs:v5.1.0/zombies/doors/get_hover_name with storage mgs:temp _door_hover

# Chip-in: door progress is GLOBAL, so the payment is mirrored onto every entity of the link group
# (both sides of every linked door) and anyone can pay the next chunk.
scoreboard players operation #door_paid mgs.data += #door_price mgs.data
execute if score #door_partial mgs.data matches 1.. as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data run scoreboard players operation @s mgs.zb.door.paid = #door_paid mgs.data
execute if score #door_partial mgs.data matches 1.. if score #door_paid mgs.data < #door_total mgs.data run return run function mgs:v5.1.0/zombies/doors/announce_progress

# Open all doors with matching link_id
execute as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data at @s run function mgs:v5.1.0/zombies/doors/open_one

# Announce (the total, not the last chunk: it's what the door cost the team)
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.opened"}],{"storage":"mgs:temp","nbt":"_door_hover_name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for"}],{"score":{"name":"#door_total","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3"}]]
function mgs:v5.1.0/zombies/feedback/sound_announce

