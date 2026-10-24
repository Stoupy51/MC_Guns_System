
#> mgs:v5.2.0/zombies/wallbuys/msg_refund_full
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.2.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ammo_is_already_full_refunded","fallback":"Ammo is already full. Refunded ","color":"red"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.points_3","fallback":"points."}]]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

