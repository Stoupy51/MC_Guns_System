
#> mgs:v5.0.0/zombies/mystery_box/deny_not_enough_points
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"#zb_mystery_box_price","objective":"mgs.config"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
function mgs:v5.0.0/zombies/feedback/sound_deny

