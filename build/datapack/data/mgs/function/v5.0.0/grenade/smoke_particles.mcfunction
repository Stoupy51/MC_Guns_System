
#> mgs:v5.0.0/grenade/smoke_particles
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/tick_effect
#

# Dense smoke cloud within effect radius
particle campfire_signal_smoke ~ ~0.5 ~ 3 2 3 0.01 20 force @a[distance=..128]
particle large_smoke ~ ~1 ~ 2 1.5 2 0.02 10 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~0.3 ~ 2.5 0.5 2.5 0.005 5 force @a[distance=..128]

