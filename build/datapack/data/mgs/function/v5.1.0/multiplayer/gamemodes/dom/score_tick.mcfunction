
#> mgs:v5.1.0/multiplayer/gamemodes/dom/score_tick
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/dom/tick
#

# Count red-owned and blue-owned points
execute store result score #dom_r mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=1}]
execute store result score #dom_b mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=2}]

# Add to team scores
scoreboard players operation #red mgs.mp.team += #dom_r mgs.data
scoreboard players operation #blue mgs.mp.team += #dom_b mgs.data

# XP for actually standing on a point your team holds, rather than for the team owning it from anywhere.
# This tick is already the 5s cadence, so it is one award per point held per 5s. Before check_team_win:
# that can end the match, and the cleanup it runs would leave nobody left to pay.
execute as @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=1}] at @s run execute as @a[distance=..5,scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_dom_hold
execute as @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=2}] at @s run execute as @a[distance=..5,scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_dom_hold

# Refresh DOM sidebar with updated point ownership
function mgs:v5.1.0/multiplayer/refresh_sidebar_dom

# Check win
function mgs:v5.1.0/multiplayer/check_team_win

