
#> mgs:v5.0.0/zombies/respawn_tp
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/perks/trigger_coward
#			mgs:v5.0.0/zombies/revive/do_round_respawn
#

execute if entity @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player] run function mgs:v5.0.0/zombies/pick_spawn

