
#> mgs:v5.0.0/projectile/realistic_explosion
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.0/projectile/explode
#

# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #rpg_explosion_power mgs.config
execute if score #rpg_explosion_power mgs.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #rpg_explosion_power mgs.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode

