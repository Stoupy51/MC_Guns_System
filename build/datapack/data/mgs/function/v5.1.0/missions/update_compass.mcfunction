
#> mgs:v5.1.0/missions/update_compass
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/game_tick [ at @s ]
#

# Only players actually carrying the mission compass need the item write
execute unless items entity @s hotbar.3 minecraft:compass run return fail

# Get nearest enemy position: ONE sorted scan + ONE NBT read, then cheap storage extracts
# (was three @n scans, each with its own distance sort and Pos read)
data modify storage mgs:temp _compass.pos set from entity @n[tag=mgs.mission_enemy] Pos
execute store result storage mgs:temp _compass.x int 1 run data get storage mgs:temp _compass.pos[0]
execute store result storage mgs:temp _compass.y int 1 run data get storage mgs:temp _compass.pos[1]
execute store result storage mgs:temp _compass.z int 1 run data get storage mgs:temp _compass.pos[2]

# Update compass in hotbar slot 3
function mgs:v5.1.0/missions/set_compass_target with storage mgs:temp _compass

