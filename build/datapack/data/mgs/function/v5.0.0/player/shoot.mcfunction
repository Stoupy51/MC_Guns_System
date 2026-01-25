
#> mgs:v5.0.0/player/shoot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#			mgs:v5.0.0/player/shoot
#

# Check which type of movement the player is doing
function mgs:v5.0.0/raycast/accuracy/get_value

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.0.0/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.0.0/player/shoot

