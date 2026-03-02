
#> mgs:v5.0.0/mob/shoot
#
# @executed	anchored eyes & facing entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] feet
#
# @within	mgs:v5.0.0/mob/fire_weapon
#			mgs:v5.0.0/mob/shoot
#

# Set accuracy (mobs use base accuracy)
data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_base

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.0.0/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.0.0/mob/shoot

