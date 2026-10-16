
#> mgs:v5.1.0/multiplayer/respawn_tp
#
# @within	mgs:v5.1.0/multiplayer/join_game
#			mgs:v5.1.0/multiplayer/actual_respawn
#

execute unless score #in_multiplayer_map mgs.data matches 1 run return run function mgs:v5.1.0/shared/enter_map {mode:"multiplayer",fn:"mgs:v5.1.0/multiplayer/respawn_tp"}

# General spawns first, against spawn camping.
execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_general] run return run function mgs:v5.1.0/multiplayer/pick_spawn {type:"general"}

# Team spawns when the map has no general ones.
execute if score @s mgs.mp.team matches 1 run return run function mgs:v5.1.0/multiplayer/pick_spawn {type:"red"}
execute if score @s mgs.mp.team matches 2 run return run function mgs:v5.1.0/multiplayer/pick_spawn {type:"blue"}

