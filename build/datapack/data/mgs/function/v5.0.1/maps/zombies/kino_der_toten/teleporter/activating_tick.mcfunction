
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/activating_tick
#
# @executed	at @e[tag=mgs.kino.teleporter_theater]
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/tick [ at @e[tag=mgs.kino.teleporter_theater] ]
#

# Count down the 50-tick activation delay
scoreboard players remove #kino_tp_timer mgs.data 1

# Kill nearby zombies each tick
kill @e[tag=mgs.zombie_round,distance=..4]

# Spawn electric_spark particles at the theater interaction entity
particle electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.1 30 normal

# Play firework sound at three points (tick 40, 25, 10)
execute if score #kino_tp_timer mgs.data matches 40 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer mgs.data matches 25 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1
execute if score #kino_tp_timer mgs.data matches 10 run playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..30] ~ ~ ~ 1 1

# When timer reaches 0, execute the actual teleport
execute if score #kino_tp_timer mgs.data matches ..0 run function mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/do_teleport

