
#> mgs:v5.0.0/projectile/realistic_explosion
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.0/projectile/explode
#

# Set explosion power from config and call the library
execute store result storage realistic_explosion:main power int 1 run scoreboard players get #rpg_explosion_power mgs.config
function realistic_explosion:explode

