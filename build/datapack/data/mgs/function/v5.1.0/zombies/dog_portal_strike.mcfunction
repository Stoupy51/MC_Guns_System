
#> mgs:v5.1.0/zombies/dog_portal_strike
#
# @executed	as @e[tag=mgs.dog_portal] & at @s
#
# @within	mgs:v5.1.0/zombies/dog_portal_tick
#

# The bolt itself: a tall, thin column drawn in one command — a wide Y spread with near-zero XZ
# spread and speed 0, so the particles fill a vertical shaft instead of puffing outward.
particle minecraft:electric_spark ~ ~4 ~ 0.06 4.0 0.06 0.0 160 force @a[distance=..64]
particle minecraft:end_rod ~ ~4 ~ 0.04 4.0 0.04 0.0 40 force @a[distance=..64]

# flash is a ColorParticleOption type, so the ARGB color is mandatory. Cold blue-white.
particle minecraft:flash{color:[1.0f,0.82f,0.90f,1.0f]} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]

# Ground shockwave: a flat disc kicked outward along the floor where the bolt lands
particle minecraft:electric_spark ~ ~0.15 ~ 1.6 0.02 1.6 0.5 90 force @a[distance=..48]
particle minecraft:crit ~ ~0.15 ~ 1.2 0.02 1.2 0.3 30 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.impact ambient @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder ambient @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

function mgs:v5.1.0/zombies/summon_dog_at

# Hand the spawn point id over to the dog, then retire the portal
scoreboard players operation @n[tag=mgs.zb_dog_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.zb_dog_new] remove mgs.zb_dog_new
scoreboard players remove #zb_dog_pending mgs.data 1
kill @s

