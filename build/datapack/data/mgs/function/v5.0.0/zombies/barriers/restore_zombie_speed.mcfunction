
#> mgs:v5.0.0/zombies/barriers/restore_zombie_speed
#
# @executed	as @e[tag=...]
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @e[tag=...] ]
#

# @s = frozen zombie — restore level-appropriate speed
attribute @s minecraft:movement_speed modifier remove mgs:freeze
tag @s remove mgs.barrier_frozen

