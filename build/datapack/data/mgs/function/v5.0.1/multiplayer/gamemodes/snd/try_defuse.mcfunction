
#> mgs:v5.0.1/multiplayer/gamemodes/snd/try_defuse
#
# @executed	at @s
#
# @within	mgs:v5.0.1/multiplayer/gamemodes/snd/tick [ at @s ]
#

# Only defenders can defuse
execute if score #snd_attackers mgs.data matches 1 unless score @s mgs.mp.team matches 2 run return fail
execute if score #snd_attackers mgs.data matches 2 unless score @s mgs.mp.team matches 1 run return fail

# Continue defusing (7.5 seconds = 150 ticks); the bomb countdown keeps running in parallel
scoreboard players set #snd_channeling mgs.data 1
scoreboard players add #snd_defuse_progress mgs.data 1
title @s actionbar [{"translate":"mgs.defusing","color":"aqua"},{"score":{"name":"#snd_defuse_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.150"}]

execute if score #snd_defuse_progress mgs.data matches 150.. run function mgs:v5.0.1/multiplayer/gamemodes/snd/bomb_defused

