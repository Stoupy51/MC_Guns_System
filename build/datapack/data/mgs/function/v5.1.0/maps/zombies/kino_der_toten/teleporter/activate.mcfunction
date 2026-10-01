
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/activate
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_theater_click [ at @s ]
#

# Run as the theater interaction.
playsound minecraft:entity.lightning_bolt.thunder block @a[distance=..50] ~ ~ ~ 0.25 1
playsound minecraft:block.portal.trigger block @a[distance=..50] ~ ~ ~ 1 2

# State 3: 50-tick build-up.
scoreboard players set #kino_tp_state mgs.data 3
scoreboard players set #kino_tp_timer mgs.data 50

