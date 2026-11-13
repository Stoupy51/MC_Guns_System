
#> mgs:v5.4.2/player/shoot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/fire_weapon
#			mgs:v5.4.2/player/shoot
#

# Accuracy depends on the movement.
function mgs:v5.4.2/raycast/accuracy/get_value

# Deadshot Daiquiri (zombies): spread to 65%.
execute if score @s mgs.special.deadshot matches 1 run function mgs:v5.4.2/raycast/accuracy/deadshot_scale

# Raycast, and a cloud particle forward.
scoreboard players set #bullet_hit mgs.data 0
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[tag=!bs.raycast.omit,distance=..32]
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.4.2/raycast/main
tag @s remove bs.raycast.omit
function mgs:v5.4.2/stats/record_bullet

scoreboard players remove #bullets_to_fire mgs.data 1
execute if score #bullets_to_fire mgs.data matches 1.. run function mgs:v5.4.2/player/shoot

