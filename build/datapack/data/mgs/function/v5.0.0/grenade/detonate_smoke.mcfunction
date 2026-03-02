
#> mgs:v5.0.0/grenade/detonate_smoke
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/detonate
#

# Activation sound
playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.extinguish_fire player @a[distance=..32] ~ ~ ~ 1 0.5

# Set duration timer (reuse the fuse score for duration countdown)
execute store result score @s mgs.data run data get entity @s data.config.grenade_duration

# Mark as active effect (skip movement in tick)
tag @s add mgs.grenade_active_effect

# Stop all velocity
scoreboard players set @s bs.vel.x 0
scoreboard players set @s bs.vel.y 0
scoreboard players set @s bs.vel.z 0

# Initial burst of smoke
particle campfire_signal_smoke ~ ~ ~ 2 1 2 0.02 30 force @a[distance=..128]

