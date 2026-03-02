
#> mgs:v5.0.0/grenade/realistic_explosion
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/detonate_frag
#

# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #grenade_explosion_power mgs.config
execute if score #grenade_explosion_power mgs.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #grenade_explosion_power mgs.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode

