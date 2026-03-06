
#> mgs:v5.0.0/multiplayer/pick_spawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/tp_all_to_spawns {type:"general"} [ at @s ]
#			mgs:v5.0.0/multiplayer/tp_all_to_spawns {type:"red"} [ at @s ]
#			mgs:v5.0.0/multiplayer/tp_all_to_spawns {type:"blue"} [ at @s ]
#			mgs:v5.0.0/multiplayer/respawn_tp {type:"general"}
#			mgs:v5.0.0/multiplayer/respawn_tp {type:"red"}
#			mgs:v5.0.0/multiplayer/respawn_tp {type:"blue"}
#
# @args		type (string)
#

# Mark this player as needing a spawn
tag @s add mgs.spawn_pending

# Tag enemy players (for distance calculation — ignore teammates)
# In FFA or team=0: all in-game players are "enemies" for spawn distance
execute if score @s mgs.mp.team matches 0 run tag @a[scores={mgs.mp.in_game=1}] add mgs.spawn_enemy
# In team modes: only tag players on different teams
execute if score @s mgs.mp.team matches 1 run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=2..}] add mgs.spawn_enemy
execute if score @s mgs.mp.team matches 2 run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=..1}] add mgs.spawn_enemy
# Never count self as an enemy
tag @s remove mgs.spawn_enemy

# Tag candidate spawn markers of the right type
$tag @e[tag=mgs.spawn_point,tag=mgs.spawn_$(type)] add mgs.spawn_candidate

# Remove candidates that have an enemy player within 5 blocks
execute as @e[tag=mgs.spawn_candidate] at @s if entity @a[tag=mgs.spawn_enemy,distance=..5] run tag @s remove mgs.spawn_candidate

# If all were removed (all spawns contested), re-tag all as candidates
$execute unless entity @e[tag=mgs.spawn_candidate] run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_$(type)] add mgs.spawn_candidate

# If no enemies, pick random candidate directly (skip expensive distance calc)
execute unless entity @a[tag=mgs.spawn_enemy] run return run function mgs:v5.0.0/multiplayer/pick_spawn_random

# Limit to X random candidates before distance computation (optimization)
tag @e[tag=mgs.spawn_candidate,sort=random,limit=32] add mgs.spawn_final
tag @e[tag=mgs.spawn_candidate,tag=!mgs.spawn_final] remove mgs.spawn_candidate
tag @e[tag=mgs.spawn_final] remove mgs.spawn_final

# Compute distance² to nearest enemy player for each candidate
execute as @e[tag=mgs.spawn_candidate] at @s run function mgs:v5.0.0/multiplayer/spawn_calc_dist

# Find the maximum distance score
scoreboard players set #_best_dist mgs.data 0
scoreboard players operation #_best_dist mgs.data > @e[tag=mgs.spawn_candidate] mgs.data

# Pick the first candidate with that best score and TP the pending player there
execute as @e[tag=mgs.spawn_candidate,sort=random] if score @s mgs.data = #_best_dist mgs.data run function mgs:v5.0.0/multiplayer/tp_to_spawn

# Clean up
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending
tag @a[tag=mgs.spawn_enemy] remove mgs.spawn_enemy

