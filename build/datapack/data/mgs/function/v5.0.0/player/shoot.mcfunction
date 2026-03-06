
#> mgs:v5.0.0/player/shoot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/fire_weapon
#			mgs:v5.0.0/player/shoot
#

# Check which type of movement the player is doing
function mgs:v5.0.0/raycast/accuracy/get_value

# Launch cloud particle forward
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[distance=..32]

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.0.0/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.0.0/player/shoot

