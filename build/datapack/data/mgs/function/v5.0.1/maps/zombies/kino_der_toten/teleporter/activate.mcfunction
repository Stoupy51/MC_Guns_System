
#> mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/activate
#
# @executed	at @s
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/teleporter/on_theater_click [ at @s ]
#

# @s = theater interaction entity (armed, state 2)
# Play activation start sound
playsound minecraft:entity.lightning_bolt.thunder block @a[distance=..50] ~ ~ ~ 0.25 1
playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2

# State 3: 30-tick activation delay (particles + sound build-up)
scoreboard players set #kino_tp_state mgs.data 3
scoreboard players set #kino_tp_timer mgs.data 30

