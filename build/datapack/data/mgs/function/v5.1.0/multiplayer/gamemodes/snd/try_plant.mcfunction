
#> mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ at @s ]
#

# Continue planting
scoreboard players set #snd_channeling mgs.data 1
scoreboard players operation #snd_plant_progress mgs.data += #tick_delta mgs.data
title @s actionbar [{"translate":"mgs.planting","color":"gold"},{"score":{"name":"#snd_plant_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100"}]

# If planted
execute if score #snd_plant_progress mgs.data matches 100.. run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted

