
#> mgs:v5.1.0/multiplayer/gamemodes/ffa/on_kill
#
# @within	mgs:v5.1.0/multiplayer/on_kill_signal
#

scoreboard players add @s mgs.mp.kills 1

function mgs:v5.1.0/multiplayer/refresh_sidebar_ffa

execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score @s mgs.mp.kills >= #score_limit mgs.data run function mgs:v5.1.0/multiplayer/gamemodes/ffa/player_wins

