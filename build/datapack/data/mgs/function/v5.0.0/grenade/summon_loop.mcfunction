
#> mgs:v5.0.0/grenade/summon_loop
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/grenade/throw
#			mgs:v5.0.0/grenade/summon_loop
#

# Summon a grenade
function mgs:v5.0.0/grenade/summon

# Loop for remaining grenades
scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.0.0/grenade/summon_loop

