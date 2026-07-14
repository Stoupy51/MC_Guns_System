
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_players
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/tick
#

# Scatter each tagged player to a random lobby position
execute as @a[tag=mgs.kino.in_tp] run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/return_one
# Keep kino.in_tp tags — needed by return_to_lobby after 5 seconds

# State 5: 5 seconds (100t) before teleporting everyone back to the lobby pad
scoreboard players set #kino_tp_state mgs.data 5
scoreboard players set #kino_tp_timer mgs.data 100

