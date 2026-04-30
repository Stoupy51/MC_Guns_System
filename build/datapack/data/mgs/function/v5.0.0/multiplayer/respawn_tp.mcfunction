
#> mgs:v5.0.0/multiplayer/respawn_tp
#
# @within	mgs:v5.0.0/multiplayer/join_game
#			mgs:v5.0.0/multiplayer/actual_respawn
#

# Try general spawns first (prevents spawn camping)
execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_general] run return run function mgs:v5.0.0/multiplayer/pick_spawn {type:"general"}

# Fallback to team spawns if map has no general spawns
execute if score @s mgs.mp.team matches 1 run return run function mgs:v5.0.0/multiplayer/pick_spawn {type:"red"}
execute if score @s mgs.mp.team matches 2 run return run function mgs:v5.0.0/multiplayer/pick_spawn {type:"blue"}

