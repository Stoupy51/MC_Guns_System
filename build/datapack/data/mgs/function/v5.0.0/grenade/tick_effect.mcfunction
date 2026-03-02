
#> mgs:v5.0.0/grenade/tick_effect
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/tick
#

# Decrement effect duration
scoreboard players remove @s mgs.data 1

# Emit smoke cloud particles
execute store result score #effect_r mgs.data run data get entity @s data.config.grenade_effect_radius
function mgs:v5.0.0/grenade/smoke_particles

# Play ambient sound occasionally (every 20 ticks)
execute store result score #smoke_tick mgs.data run scoreboard players get @s mgs.data
scoreboard players operation #smoke_tick mgs.data %= #20 mgs.data
execute if score #smoke_tick mgs.data matches 0 run playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 0.3 0.5

# If duration expired, delete
execute if score @s mgs.data matches ..0 run function mgs:v5.0.0/grenade/delete

