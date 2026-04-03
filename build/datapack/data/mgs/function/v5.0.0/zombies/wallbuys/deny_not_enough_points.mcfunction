
#> mgs:v5.0.0/zombies/wallbuys/deny_not_enough_points
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
function mgs:v5.0.0/zombies/feedback/sound_deny

