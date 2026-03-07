
#> mgs:v5.0.0/multiplayer/gamemodes/dom/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Process each domination point
execute as @e[tag=mgs.dom_point] at @s run function mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick

# Sync point ownership to global scores for sidebar display
execute as @e[tag=mgs.dom_point,tag=mgs.dom_label_A] store result score #dom_owner_a mgs.data run scoreboard players get @s mgs.mp.dom_owner
execute as @e[tag=mgs.dom_point,tag=mgs.dom_label_B] store result score #dom_owner_b mgs.data run scoreboard players get @s mgs.mp.dom_owner
execute as @e[tag=mgs.dom_point,tag=mgs.dom_label_C] store result score #dom_owner_c mgs.data run scoreboard players get @s mgs.mp.dom_owner
execute as @e[tag=mgs.dom_point,tag=mgs.dom_label_D] store result score #dom_owner_d mgs.data run scoreboard players get @s mgs.mp.dom_owner
execute as @e[tag=mgs.dom_point,tag=mgs.dom_label_E] store result score #dom_owner_e mgs.data run scoreboard players get @s mgs.mp.dom_owner

# Scoring interval
scoreboard players remove #dom_score_timer mgs.data 1
execute if score #dom_score_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick
execute if score #dom_score_timer mgs.data matches ..0 run scoreboard players set #dom_score_timer mgs.data 100

# Show particles at each point
execute as @e[tag=mgs.dom_point] at @s run function mgs:v5.0.0/multiplayer/gamemodes/dom/point_particles

