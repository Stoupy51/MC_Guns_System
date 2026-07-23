
#> mgs:v5.1.0/zombies/wallbuys/msg_purchased
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_right_click
#			mgs:v5.1.0/zombies/wallbuys/buy_knife
#			mgs:v5.1.0/zombies/wallbuys/buy_lethal
#			mgs:v5.1.0/zombies/wallbuys/buy_tactical
#			mgs:v5.1.0/zombies/wallbuys/buy_lethal_web
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_bought","color":"green"},{"storage":"mgs:temp","nbt":"_wb_display_name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for"}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3"}]]
function mgs:v5.1.0/zombies/feedback/sound_success

