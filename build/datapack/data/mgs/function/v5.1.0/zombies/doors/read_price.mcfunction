
#> mgs:v5.1.0/zombies/doors/read_price
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.1.0/zombies/doors/on_right_click
#			mgs:v5.1.0/zombies/doors/on_hover
#

execute store result score #door_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.price
execute store result score #door_partial mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.partial
execute store result score #door_paid mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.door.paid
scoreboard players operation #door_total mgs.data = #door_price mgs.data

# Remaining, clamped at 0 so a price lowered below the progress can't hand out points
scoreboard players operation #door_left mgs.data = #door_total mgs.data
scoreboard players operation #door_left mgs.data -= #door_paid mgs.data
execute if score #door_left mgs.data matches ..0 run scoreboard players set #door_left mgs.data 0

# Fixed chunks, last one is the remainder
execute if score #door_partial mgs.data matches 1.. run scoreboard players operation #door_price mgs.data = #door_partial mgs.data
execute if score #door_partial mgs.data matches 1.. run scoreboard players operation #door_price mgs.data < #door_left mgs.data

