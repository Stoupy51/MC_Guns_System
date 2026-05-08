
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/activate
#
# @executed	at @s
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/on_theater_click [ at @s ]
#

# @s = theater interaction entity (armed, state 2)
# Tag all nearby in-game players (within 3 blocks)
tag @a[distance=..3,scores={mgs.zb.in_game=1},gamemode=!spectator] add mgs.kino.in_tp

# Teleport tagged players to the projection room
execute positioned ~57 ~1 ~-9 run tp @a[tag=mgs.kino.in_tp] ~-22 ~6 ~0

# State 3: players in projection room, 600t (30s) countdown
scoreboard players set #kino_tp_state mgs.data 3
scoreboard players set #kino_tp_timer mgs.data 600

