
#> mgs:v5.0.0/grenade/stick_to_entity
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/on_stick
#

# Increment the global semtex pairing counter to get a unique ID
scoreboard players add #semtex_id mgs.data 1

# Assign the same unique ID to both the grenade and the nearest entity
scoreboard players operation @s mgs.stuck_id = #semtex_id mgs.data
execute positioned ~ ~-1 ~ run scoreboard players operation @n[type=!#mgs:ignore,distance=..2,tag=!mgs.grenade,tag=!mgs.slow_bullet,tag=!global.ignore.kill,tag=!global.ignore,nbt=!{Invulnerable:true}] mgs.stuck_id = #semtex_id mgs.data

# Mark that this grenade is stuck to an entity (not just a block)
tag @s add mgs.stuck_to_entity

