
#> mgs:v5.0.0/projectile/summon_loop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/fire_weapon
#			mgs:v5.0.0/projectile/summon_loop
#			mgs:v5.0.0/mob/fire_weapon
#

# Summon a projectile
function mgs:v5.0.0/projectile/summon

# Loop for remaining pellets
scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.0.0/projectile/summon_loop

