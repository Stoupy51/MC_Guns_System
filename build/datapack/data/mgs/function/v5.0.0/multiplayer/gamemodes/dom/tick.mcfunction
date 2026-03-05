
#> mgs:v5.0.0/multiplayer/gamemodes/dom/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Process each domination point
execute as @e[tag=mgs.dom_point] at @s run function mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick

# Scoring interval
scoreboard players remove #dom_score_timer mgs.data 1
execute if score #dom_score_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick
execute if score #dom_score_timer mgs.data matches ..0 run scoreboard players set #dom_score_timer mgs.data 100

# Show particles at each point
execute as @e[tag=mgs.dom_point] at @s run function mgs:v5.0.0/multiplayer/gamemodes/dom/point_particles

