
#> mgs:v5.4.1/missions/respawn_tp
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/missions/join_game
#			mgs:v5.4.1/missions/actual_respawn
#

execute unless score #in_missions_map mgs.data matches 1 run return run function mgs:v5.4.1/shared/enter_map {mode:"missions",fn:"mgs:v5.4.1/missions/respawn_tp"}

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_mission] run function mgs:v5.4.1/missions/pick_spawn

