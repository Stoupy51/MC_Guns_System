
#> mgs:v5.1.0/zombies/wunderfizz/deny_not_enough_points
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/try_use
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"#wf_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

