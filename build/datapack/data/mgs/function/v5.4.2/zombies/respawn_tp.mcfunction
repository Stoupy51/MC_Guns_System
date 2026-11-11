
#> mgs:v5.4.2/zombies/respawn_tp
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/join_game
#			mgs:v5.4.2/zombies/perks/trigger_coward
#

execute unless score #in_zombies_map mgs.data matches 1 run return run function mgs:v5.4.2/shared/enter_map {mode:"zombies",fn:"mgs:v5.4.2/zombies/respawn_tp"}

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player] run function mgs:v5.4.2/zombies/pick_spawn

