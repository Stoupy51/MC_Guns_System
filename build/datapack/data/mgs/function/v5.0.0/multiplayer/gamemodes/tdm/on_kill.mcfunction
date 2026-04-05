
#> mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill
#
# @within	mgs:v5.0.0/multiplayer/on_kill_signal
#

scoreboard players add @s mgs.mp.kills 1
execute if score @s mgs.mp.team matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score @s mgs.mp.team matches 2 run scoreboard players add #blue mgs.mp.team 1

# Refresh sidebar to show updated team scores
function #bs.sidebar:refresh {objective:"mgs.sidebar"}

# Check win condition
function mgs:v5.0.0/multiplayer/check_team_win

