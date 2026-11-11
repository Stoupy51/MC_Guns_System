
#> mgs:v5.4.2/multiplayer/respawn_tp
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/join_game
#			mgs:v5.4.2/multiplayer/actual_respawn
#

execute unless score #in_multiplayer_map mgs.data matches 1 run return run function mgs:v5.4.2/shared/enter_map {mode:"multiplayer",fn:"mgs:v5.4.2/multiplayer/respawn_tp"}

# General spawns first, against spawn camping.
execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_general] run return run function mgs:v5.4.2/multiplayer/pick_spawn {type:"general"}

# Team spawns when the map has no general ones.
execute if score @s mgs.mp.team matches 1 run return run function mgs:v5.4.2/multiplayer/pick_spawn {type:"red"}
execute if score @s mgs.mp.team matches 2 run return run function mgs:v5.4.2/multiplayer/pick_spawn {type:"blue"}

