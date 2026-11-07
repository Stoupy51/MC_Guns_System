
#> mgs:v5.4.0/mob/shoot
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/mob/fire_weapon
#			mgs:v5.4.0/mob/shoot
#

# Mobs use the base accuracy.
data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_base

tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.4.0/raycast/main
tag @s remove bs.raycast.omit

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.4.0/mob/shoot

