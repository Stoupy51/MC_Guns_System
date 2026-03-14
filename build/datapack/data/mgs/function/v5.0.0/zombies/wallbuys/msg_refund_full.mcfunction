
#> mgs:v5.0.0/zombies/wallbuys/msg_refund_full
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.ammo_is_already_full_refunded","color":"red"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.points_2"}]]
function mgs:v5.0.0/zombies/feedback/sound_deny

