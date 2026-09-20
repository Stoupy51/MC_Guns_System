
#> mgs:v5.1.0/zombies/respawn_tp
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/join_game
#			mgs:v5.1.0/zombies/perks/trigger_coward
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player] run function mgs:v5.1.0/zombies/pick_spawn

