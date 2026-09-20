
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/do_teleport
#
# @executed	at @e[tag=mgs.kino.teleporter_theater]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/activating_tick
#

# Tag all nearby in-game players (within 3 blocks) and teleport to the projection room
tag @a[distance=..3,scores={mgs.zb.in_game=1},gamemode=!spectator] add mgs.kino.in_tp
execute positioned ~57 ~1 ~-9 run tp @a[tag=mgs.kino.in_tp] ~-22 ~6 ~0
execute as @a[tag=mgs.kino.in_tp] at @s run playsound minecraft:entity.enderman.teleport block @s ~ ~ ~ 1 1

# State 4: players in projection room, 600t (30s) countdown
scoreboard players set #kino_tp_state mgs.data 4
scoreboard players set #kino_tp_timer mgs.data 600

