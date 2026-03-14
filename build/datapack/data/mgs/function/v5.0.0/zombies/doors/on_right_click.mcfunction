
#> mgs:v5.0.0/zombies/doors/on_right_click
#
# @within	???
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Get door price from interacted entity
execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price

# Check player has enough points
execute unless score @s mgs.zb.points >= #door_price mgs.data run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":" ","color":"red"}, {"translate":"mgs.not_enough_points"}]]

# Deduct points
scoreboard players operation @s mgs.zb.points -= #door_price mgs.data

# Get link_id from interacted door
execute store result score #door_link mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.link

# Open all doors with matching link_id
execute as @e[tag=mgs.door] if score @s mgs.zb.door.link = #door_link mgs.data at @s run function mgs:v5.0.0/zombies/doors/open_one

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":" 🚪 ","color":"green"}, {"translate":"mgs.door_opened"}]]

