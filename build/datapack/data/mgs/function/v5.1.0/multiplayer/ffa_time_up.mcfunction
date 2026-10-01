
#> mgs:v5.1.0/multiplayer/ffa_time_up
#
# @within	mgs:v5.1.0/multiplayer/time_up
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.times_up","color":"gold"}]

scoreboard players set #max_kills mgs.data 0
scoreboard players operation #max_kills mgs.data > @a[scores={mgs.mp.in_game=1}] mgs.mp.kills

execute as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.kills = #max_kills mgs.data run function mgs:v5.1.0/multiplayer/gamemodes/ffa/player_wins

