
#> mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/return_players
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/tick
#

execute as @a[tag=mgs.kino.in_tp] run function mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/return_one
# kino.in_tp stays: return_to_lobby needs it 5 s later.

scoreboard players set #kino_tp_state mgs.data 5
scoreboard players set #kino_tp_timer mgs.data 100

