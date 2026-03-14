
#> mgs:v5.0.0/zombies/doors/on_right_click
#
# @within	???
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Get door price from interacted entity
execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price

# Check player has enough points
execute unless score @s mgs.zb.points >= #door_price mgs.data run return run function mgs:v5.0.0/zombies/doors/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #door_price mgs.data

# Get link_id from interacted door
execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link

# Open all doors with matching link_id
execute as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data at @s run function mgs:v5.0.0/zombies/doors/open_one

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.door_opened_for","color":"green"},{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_2"}]]
function mgs:v5.0.0/zombies/feedback/sound_announce

