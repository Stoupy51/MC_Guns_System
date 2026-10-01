
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/activating_tick
#
# @executed	at @e[tag=mgs.kino.teleporter_theater]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/tick [ at @e[tag=mgs.kino.teleporter_theater] ]
#

scoreboard players remove #kino_tp_timer mgs.data 1

kill @e[tag=mgs.zombie_round,distance=..4]

particle electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.1 30 normal

# Firework cue at ticks 40, 25 and 10.
execute if score #kino_tp_timer mgs.data matches 40 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer mgs.data matches 25 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer mgs.data matches 10 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1

execute if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/do_teleport

