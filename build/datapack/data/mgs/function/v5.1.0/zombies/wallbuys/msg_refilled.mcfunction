
#> mgs:v5.1.0/zombies/wallbuys/msg_refilled
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_right_click
#			mgs:v5.1.0/zombies/wallbuys/refill_lethal
#			mgs:v5.1.0/zombies/wallbuys/refill_tactical
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.ammo_refilled_for","color":"gold"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_3"}]]
playsound minecraft:block.note_block.pling ambient @s ~ ~ ~ 0.8 1.45

