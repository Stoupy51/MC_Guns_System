
#> mgs:v5.1.0/multiplayer/gamemodes/snd/try_defuse
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ at @s ]
#

execute if score #snd_attackers mgs.data matches 1 unless score @s mgs.mp.team matches 2 run return fail
execute if score #snd_attackers mgs.data matches 2 unless score @s mgs.mp.team matches 1 run return fail

# The tick owns the increment, so extra defenders give cover, not a faster defuse; the fuse keeps running.
scoreboard players set #snd_channeling mgs.data 1
tag @s add mgs.xp_earner
title @s actionbar [{"translate":"mgs.defusing","color":"aqua"},{"score":{"name":"#snd_defuse_progress","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.150"}]

