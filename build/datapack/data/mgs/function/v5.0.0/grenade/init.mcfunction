
#> mgs:v5.0.0/grenade/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.0.0/grenade/summon [ anchored eyes & positioned ^ ^ ^0.5 ]
#

# Tag as grenade
tag @s add mgs.grenade

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

# Copy grenade config from temp storage
data modify entity @s data.config set from storage mgs:temp grenade

# Set the visual model on the item_display entity
function mgs:v5.0.0/grenade/set_model with entity @s data.config

# Set fuse timer from config
execute store result score @s mgs.data run data get entity @s data.config.grenade_fuse

# Launch grace period: disable entity collision for 3 ticks to avoid sticking to the thrower
scoreboard players set @s mgs.grenade_launch 3

# Calculate velocity from the player's look direction and teleport back
function mgs:v5.0.0/shared/calc_velocity

