
#> mgs:v5.1.0/grenade/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.1.0/grenade/summon [ anchored eyes & positioned ^ ^ ^0.5 ]
#

tag @s add mgs.grenade

# For damage attribution.
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

data modify entity @s data.config set from storage mgs:temp grenade

# Camo variants override the base model.
function mgs:v5.1.0/grenade/set_model with entity @s data.config
execute if data entity @s data.config.model_override run function mgs:v5.1.0/grenade/set_model_override with entity @s data.config

execute store result score @s mgs.data run data get entity @s data.config.grenade_fuse

# The zombies module owns the attraction.
execute if data entity @s data.config{grenade_type:"monkey_bomb"} run function mgs:v5.1.0/zombies/monkey/on_throw

# No entity collision for 3 ticks, so it never sticks to the thrower.
scoreboard players set @s mgs.grenade_launch 3

# From the look direction, then back.
function mgs:v5.1.0/shared/calc_velocity

