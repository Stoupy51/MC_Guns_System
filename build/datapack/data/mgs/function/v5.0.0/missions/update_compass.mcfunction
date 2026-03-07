
#> mgs:v5.0.0/missions/update_compass
#
# @executed	at @s
#
# @within	mgs:v5.0.0/missions/game_tick [ at @s ]
#

# Skip if no enemies remain
execute unless entity @e[tag=mgs.mission_enemy] run return fail

# Get nearest enemy position as ints
execute store result storage mgs:temp _compass.x int 1 run data get entity @n[tag=mgs.mission_enemy] Pos[0]
execute store result storage mgs:temp _compass.y int 1 run data get entity @n[tag=mgs.mission_enemy] Pos[1]
execute store result storage mgs:temp _compass.z int 1 run data get entity @n[tag=mgs.mission_enemy] Pos[2]

# Update compass in hotbar slot 3
function mgs:v5.0.0/missions/set_compass_target with storage mgs:temp _compass

