
#> mgs:v5.0.1/zombies/respawn_tp
#
# @within	mgs:v5.0.1/zombies/join_game
#			mgs:v5.0.1/zombies/perks/trigger_coward
#			mgs:v5.0.1/zombies/revive/do_round_respawn
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player] run function mgs:v5.0.1/zombies/pick_spawn

