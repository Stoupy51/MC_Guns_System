
#> mgs:v5.1.0/zombies/dog_portal_strike
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/dog_portal_tick
#

# A wide Y spread with near-zero XZ spread and speed 0 draws a vertical shaft.
particle minecraft:electric_spark ~ ~4 ~ 0.06 4.0 0.06 0.0 160 force @a[distance=..64]
particle minecraft:end_rod ~ ~4 ~ 0.04 4.0 0.04 0.0 40 force @a[distance=..64]

# flash takes a mandatory ARGB color.
particle minecraft:flash{color:[1.0f,0.82f,0.90f,1.0f]} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]

particle minecraft:electric_spark ~ ~0.15 ~ 1.6 0.02 1.6 0.5 90 force @a[distance=..48]
particle minecraft:crit ~ ~0.15 ~ 1.2 0.02 1.2 0.3 30 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.impact ambient @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder ambient @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

function mgs:v5.1.0/zombies/summon_dog_at

scoreboard players operation @n[tag=mgs.zb_dog_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.zb_dog_new] remove mgs.zb_dog_new
scoreboard players remove #zb_dog_pending mgs.data 1
kill @s

