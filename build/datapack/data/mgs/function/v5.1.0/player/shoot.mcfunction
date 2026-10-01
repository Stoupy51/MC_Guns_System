
#> mgs:v5.1.0/player/shoot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/fire_weapon
#			mgs:v5.1.0/player/shoot
#

# Accuracy depends on the movement.
function mgs:v5.1.0/raycast/accuracy/get_value

# Deadshot Daiquiri (zombies): spread to 65%.
execute if score @s mgs.special.deadshot matches 1 run function mgs:v5.1.0/raycast/accuracy/deadshot_scale

# Raycast, and a cloud particle forward.
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[tag=!bs.raycast.omit,distance=..32]
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.1.0/raycast/main
tag @s remove bs.raycast.omit

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.1.0/player/shoot

