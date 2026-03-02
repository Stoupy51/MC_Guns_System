
#> mgs:v5.0.0/projectile/match_shooter
#
# @executed	as @a
#
# @within	mgs:v5.0.0/projectile/explode [ as @a ]
#			mgs:v5.0.0/grenade/detonate_frag [ as @a ]
#

# Compare this player's UUID with the stored shooter UUID
# data modify returns 0 (no change) when values are identical, 1 when modified
data modify storage mgs:temp copy_uuid set from entity @s UUID
execute store success score #is_match mgs.data run data modify storage mgs:temp copy_uuid set from storage mgs:temp expl.shooter_uuid

# If #is_match is 0, the UUIDs were identical (no change was made), so this is the shooter
execute if score #is_match mgs.data matches 0 run tag @s add mgs.temp_shooter

