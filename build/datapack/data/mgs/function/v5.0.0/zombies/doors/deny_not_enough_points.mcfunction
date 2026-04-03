
#> mgs:v5.0.0/zombies/doors/deny_not_enough_points
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.0.0/zombies/doors/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
function mgs:v5.0.0/zombies/feedback/sound_deny

