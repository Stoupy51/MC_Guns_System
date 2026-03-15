
#> mgs:v5.0.0/zombies/wallbuys/msg_purchased
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_bought","color":"green"},{"storage":"mgs:temp","nbt":"_wb_weapon.name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.for"}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_3"}]]
function mgs:v5.0.0/zombies/feedback/sound_success

