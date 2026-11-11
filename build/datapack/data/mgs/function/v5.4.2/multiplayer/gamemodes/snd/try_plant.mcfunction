
#> mgs:v5.4.2/multiplayer/gamemodes/snd/try_plant
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/gamemodes/snd/tick [ at @s ]
#

scoreboard players set #snd_channeling mgs.data 1
title @s actionbar [{"translate":"mgs.planting","fallback":"Planting... ","color":"gold"},{"score":{"name":"#snd_plant_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100","fallback":"/100"}]

