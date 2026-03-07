
#> mgs:v5.0.0/multiplayer/gamemodes/dom/on_kill
#
# @within	mgs:v5.0.0/multiplayer/on_kill_signal
#

scoreboard players add @s mgs.mp.kills 1
execute if score @s mgs.mp.team matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score @s mgs.mp.team matches 2 run scoreboard players add #blue mgs.mp.team 1

# Refresh DOM sidebar to show updated team scores and point ownership
function mgs:v5.0.0/multiplayer/refresh_sidebar_dom

