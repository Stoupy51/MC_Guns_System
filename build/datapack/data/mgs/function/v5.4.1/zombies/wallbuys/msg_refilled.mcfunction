
#> mgs:v5.4.1/zombies/wallbuys/msg_refilled
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/wallbuys/on_right_click
#			mgs:v5.4.1/zombies/wallbuys/refill_lethal
#			mgs:v5.4.1/zombies/wallbuys/refill_tactical
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ammo_refilled_for","fallback":"Ammo refilled for ","color":"gold"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_3","fallback":"points."}]]
playsound minecraft:block.note_block.pling ambient @s ~ ~ ~ 0.8 1.45

