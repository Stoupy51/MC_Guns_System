
#> mgs:v5.0.0/zombies/wallbuys/msg_refilled
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.ammo_refilled_for","color":"gold"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_3"}]]
function mgs:v5.0.0/zombies/feedback/sound_refill

