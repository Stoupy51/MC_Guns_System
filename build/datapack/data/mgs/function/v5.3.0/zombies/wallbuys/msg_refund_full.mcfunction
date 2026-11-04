
#> mgs:v5.3.0/zombies/wallbuys/msg_refund_full
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ammo_is_already_full_refunded","fallback":"Ammo is already full. Refunded ","color":"red"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.points_3","fallback":"points."}]]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

