
#> mgs:v5.4.2/multiplayer/ffa_time_up
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/time_up
#

tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.times_up","fallback":"Time's up!","color":"gold"}]

scoreboard players set #max_kills mgs.data 0
scoreboard players operation #max_kills mgs.data > @a[scores={mgs.mp.in_game=1}] mgs.mp.kills

execute as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.kills = #max_kills mgs.data run function mgs:v5.4.2/multiplayer/gamemodes/ffa/player_wins

