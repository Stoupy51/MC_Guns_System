
#> mgs:v5.1.0/missions/pick_spawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/tp_all_to_spawns [ at @s ]
#			mgs:v5.1.0/missions/respawn_tp
#

tag @s add mgs.spawn_pending

# Tag candidate spawns (exclude used). Capture via command success whether any marker was tagged,
# so the "all used" fallback can branch on a score instead of a global @e existence scan.
execute store success score #has_candidate mgs.data run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_mission,tag=!mgs.spawn_used] add mgs.spawn_candidate

# If all used, re-tag all
execute if score #has_candidate mgs.data matches 0 run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_mission] add mgs.spawn_candidate

# Pick random candidate
execute as @n[tag=mgs.spawn_candidate,sort=random] run function mgs:v5.1.0/missions/tp_to_spawn

# Cleanup
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

