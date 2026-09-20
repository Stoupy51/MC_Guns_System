
#> mgs:v5.1.0/grenade/tick_stuck
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.1.0/grenade/tick
#

# If stuck to an entity, follow it
execute if entity @s[tag=mgs.stuck_to_entity] run function mgs:v5.1.0/grenade/follow_entity

# Decrement fuse timer (real-time via #tick_delta)
scoreboard players operation @s mgs.data -= #tick_delta mgs.data

# Blinking particle to indicate it's about to explode
particle small_flame ~ ~0.3 ~ 0 0 0 0 1 force @a[distance=..32]

# If fuse expired, detonate
execute if score @s mgs.data matches ..0 run function mgs:v5.1.0/grenade/detonate

