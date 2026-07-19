
#> mgs:v5.1.0/zombies/dog_portal_strike
#
# @executed	as @e[tag=mgs.dog_portal] & at @s
#
# @within	mgs:v5.1.0/zombies/dog_portal_tick
#

# flash is a ColorParticleOption type, so the ARGB color is mandatory. Cold blue-white.
particle minecraft:flash{color:[1.0f,0.82f,0.90f,1.0f]} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]
particle minecraft:electric_spark ~ ~1.2 ~ 0.25 1.4 0.25 0.35 70 force @a[distance=..48]
particle minecraft:end_rod ~ ~1 ~ 0.1 0.8 0.1 0.02 12 force @a[distance=..48]
# weather category: where lightning belongs, and a slider players rarely turn down (hostile is
# commonly lowered to mute zombie groans).
# Volume sets the audible RADIUS (1.0 = 16 blocks), not loudness, so it has to cover the selector
# range or distant players are targeted but hear nothing. The trailing minVolume is the floor
# players outside that radius still hear, so a hound spawning across the map is never silent.
playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

# Same level buckets as zombies, so the type dispatch signature stays uniform
execute if score #zb_round mgs.data matches ..5 run data modify storage mgs:temp _zpos.level set value "1"
execute if score #zb_round mgs.data matches 6..10 run data modify storage mgs:temp _zpos.level set value "2"
execute if score #zb_round mgs.data matches 11..15 run data modify storage mgs:temp _zpos.level set value "3"
execute if score #zb_round mgs.data matches 16.. run data modify storage mgs:temp _zpos.level set value "4"
function mgs:v5.1.0/zombies/summon_dog_at with storage mgs:temp _zpos

# Hand the spawn point id over to the dog, then retire the portal
scoreboard players operation @n[tag=mgs.zb_dog_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.zb_dog_new] remove mgs.zb_dog_new
scoreboard players remove #zb_dog_pending mgs.data 1
kill @s

