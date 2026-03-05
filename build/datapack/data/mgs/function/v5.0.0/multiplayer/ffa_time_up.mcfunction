
#> mgs:v5.0.0/multiplayer/ffa_time_up
#
# @within	mgs:v5.0.0/multiplayer/time_up
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.times_up","color":"gold"}]
# Store max kills into a score
scoreboard players set #_max_kills mgs.data 0
execute as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.kills > #_max_kills mgs.data run scoreboard players operation #_max_kills mgs.data = @s mgs.mp.kills
# The player with that score wins
execute as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.kills = #_max_kills mgs.data run function mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins

