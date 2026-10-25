
#> mgs:v5.3.0/zombies/wallbuys/msg_purchased
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.3.0/zombies/wallbuys/on_right_click
#			mgs:v5.3.0/zombies/wallbuys/buy_knife
#			mgs:v5.3.0/zombies/wallbuys/buy_lethal
#			mgs:v5.3.0/zombies/wallbuys/buy_tactical
#			mgs:v5.3.0/zombies/wallbuys/buy_lethal_web
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_bought","fallback":"You bought ","color":"green"},{"storage":"mgs:temp","nbt":"_wb_display_name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for","fallback":"for "}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3","fallback":"points."}]]
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

