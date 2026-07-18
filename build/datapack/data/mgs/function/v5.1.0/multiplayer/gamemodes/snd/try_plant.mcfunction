
#> mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ at @s ]
#

# Only attackers can plant
execute if score #snd_attackers mgs.data matches 1 unless score @s mgs.mp.team matches 1 run return fail
execute if score #snd_attackers mgs.data matches 2 unless score @s mgs.mp.team matches 2 run return fail

# Continue planting (5 seconds = 100 ticks)
scoreboard players set #snd_channeling mgs.data 1
scoreboard players operation #snd_plant_progress mgs.data += #tick_delta mgs.data
title @s actionbar [{"translate":"mgs.planting","color":"gold"},{"score":{"name":"#snd_plant_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100_2"}]

# If planted
execute if score #snd_plant_progress mgs.data matches 100.. run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted

