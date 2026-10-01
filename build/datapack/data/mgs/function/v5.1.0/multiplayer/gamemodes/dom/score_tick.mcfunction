
#> mgs:v5.1.0/multiplayer/gamemodes/dom/score_tick
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/dom/tick
#

execute store result score #dom_r mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=1}]
execute store result score #dom_b mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=2}]

scoreboard players operation #red mgs.mp.team += #dom_r mgs.data
scoreboard players operation #blue mgs.mp.team += #dom_b mgs.data

# XP for standing on a held point, once per point per 5 s. Before check_team_win, which can end the match and leave nobody to pay.
execute as @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=1}] at @s run execute as @a[distance=..5,scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_dom_hold
execute as @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=2}] at @s run execute as @a[distance=..5,scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_dom_hold

function mgs:v5.1.0/multiplayer/refresh_sidebar_dom

function mgs:v5.1.0/multiplayer/check_team_win

