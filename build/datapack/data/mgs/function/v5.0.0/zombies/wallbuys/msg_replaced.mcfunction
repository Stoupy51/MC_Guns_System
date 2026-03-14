
#> mgs:v5.0.0/zombies/wallbuys/msg_replaced
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.swapped_your_selected_weapon_for","color":"yellow"},{"storage":"mgs:temp","nbt":"_wb_weapon.name","color":"gold"},{"text":" (","color":"yellow"},{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"yellow"}, {"translate":"mgs.points_4"}, ")."]]
function mgs:v5.0.0/zombies/feedback/sound_replace

