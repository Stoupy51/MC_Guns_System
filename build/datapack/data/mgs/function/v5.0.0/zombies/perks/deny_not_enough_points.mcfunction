
#> mgs:v5.0.0/zombies/perks/deny_not_enough_points
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"#pk_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
function mgs:v5.0.0/zombies/feedback/sound_deny

