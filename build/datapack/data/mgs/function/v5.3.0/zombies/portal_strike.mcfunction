
#> mgs:v5.3.0/zombies/portal_strike
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/portal_tick
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

# Delivered at ground level and awake, so no rise.
data modify storage mgs:temp _mob set from entity @s data.mob
data modify storage mgs:temp _mob.no_ai set value 0b
scoreboard players operation #zb_spawn_sid mgs.data = @s mgs.zb.spawn.sid
execute store result score #zb_spawn_x mgs.data run data get entity @s Pos[0]
execute store result score #zb_spawn_z mgs.data run data get entity @s Pos[2]
execute positioned ~ ~0.2 ~ run function mgs:v5.3.0/zombies/mob/spawn
function mgs:v5.3.0/zombies/arrival/land

scoreboard players remove #zb_portal_pending mgs.data 1
kill @s

