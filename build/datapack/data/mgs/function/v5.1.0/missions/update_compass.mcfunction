
#> mgs:v5.1.0/missions/update_compass
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/game_tick [ at @s ]
#

# Only players actually carrying the mission compass need the item write
execute unless items entity @s hotbar.3 minecraft:compass run return fail

# One sorted scan, then a marker carries the position out instead of serializing the mob
execute at @n[tag=mgs.mission_enemy] summon minecraft:marker run function mgs:v5.1.0/shared/probe_pos
execute store result storage mgs:temp _compass.x int 1 run data get storage mgs:temp _probe_pos[0]
execute store result storage mgs:temp _compass.y int 1 run data get storage mgs:temp _probe_pos[1]
execute store result storage mgs:temp _compass.z int 1 run data get storage mgs:temp _probe_pos[2]

# Update compass in hotbar slot 3
function mgs:v5.1.0/missions/set_compass_target with storage mgs:temp _compass

