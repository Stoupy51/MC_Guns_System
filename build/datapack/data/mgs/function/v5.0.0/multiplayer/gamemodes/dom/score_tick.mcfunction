
#> mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/tick
#

# Count red-owned and blue-owned points
execute store result score #dom_r mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=1}]
execute store result score #dom_b mgs.data if entity @e[tag=mgs.dom_point,scores={mgs.mp.dom_owner=2}]

# Add to team scores
scoreboard players operation #red mgs.mp.team += #dom_r mgs.data
scoreboard players operation #blue mgs.mp.team += #dom_b mgs.data

# Refresh DOM sidebar with updated point ownership
function mgs:v5.0.0/multiplayer/refresh_sidebar_dom

# Check win
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score #red mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}

