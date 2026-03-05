
#> mgs:v5.0.0/multiplayer/gamemodes/ffa/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Check each player's kill count against score limit
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute as @a if score @s mgs.mp.kills >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins

