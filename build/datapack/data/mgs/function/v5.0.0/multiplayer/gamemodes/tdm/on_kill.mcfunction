
#> mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill
#
# @within	mgs:v5.0.0/multiplayer/on_kill_signal
#

scoreboard players add @s mgs.mp.kills 1
execute if score @s mgs.mp.team matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score @s mgs.mp.team matches 2 run scoreboard players add #blue mgs.mp.team 1

# Check win condition
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score #red mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}

