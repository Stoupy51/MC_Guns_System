
#> mgs:v5.1.0/mob/shoot
#
# @executed	anchored eyes & facing entity @e[tag=mgs.target,limit=1] feet
#
# @within	mgs:v5.1.0/mob/fire_weapon
#			mgs:v5.1.0/mob/shoot
#

# Mobs use the base accuracy.
data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_base

tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.1.0/raycast/main
tag @s remove bs.raycast.omit

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.1.0/mob/shoot

