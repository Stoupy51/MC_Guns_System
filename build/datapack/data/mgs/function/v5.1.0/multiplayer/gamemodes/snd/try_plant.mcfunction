
#> mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ at @s ]
#

scoreboard players set #snd_channeling mgs.data 1
title @s actionbar [{"translate":"mgs.planting","color":"gold"},{"score":{"name":"#snd_plant_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100"}]

