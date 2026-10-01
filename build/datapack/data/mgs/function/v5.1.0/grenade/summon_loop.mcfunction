
#> mgs:v5.1.0/grenade/summon_loop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/grenade/throw
#			mgs:v5.1.0/grenade/summon_loop
#

function mgs:v5.1.0/grenade/summon

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.1.0/grenade/summon_loop

