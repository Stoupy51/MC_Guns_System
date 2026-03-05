
#> mgs:v5.0.0/multiplayer/gamemodes/snd/try_plant
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/tick [ at @s ]
#

# Only attackers can plant
execute if score #snd_attackers mgs.data matches 1 unless score @s mgs.mp.team matches 1 run return fail
execute if score #snd_attackers mgs.data matches 2 unless score @s mgs.mp.team matches 2 run return fail

# Start or continue planting (5 seconds = 100 ticks)
scoreboard players set #snd_bomb_state mgs.data 1
scoreboard players add #snd_bomb_timer mgs.data 1
title @s actionbar [{"translate": "mgs.planting","color":"gold"},{"score":{"name":"#snd_bomb_timer","objective":"mgs.data"},"color":"yellow"},{"translate": "mgs.100"}]

# If planted
execute if score #snd_bomb_timer mgs.data matches 100.. run function mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_planted

