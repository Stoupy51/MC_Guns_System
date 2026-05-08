
#> mgs:v5.0.1/grenade/smoke_particles
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.1/grenade/tick_effect
#

# Dense smoke cloud within effect radius
particle campfire_signal_smoke ~ ~0.5 ~ 2 1.5 2 0.01 50 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~1 ~ 1.5 1 1.5 0.02 20 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~0.3 ~ 2 0.5 2 0.005 10 force @a[distance=..128]

