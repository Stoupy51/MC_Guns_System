
#> mgs:v5.0.0/zombies/pick_spawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/tp_all_to_spawns [ at @s ]
#			mgs:v5.0.0/zombies/respawn_tp
#

tag @s add mgs.spawn_pending

# Tag candidate spawns (unlocked, exclude used)
tag @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked,tag=!mgs.spawn_used] add mgs.spawn_candidate

# If all used, re-tag all unlocked
execute unless entity @e[tag=mgs.spawn_candidate] run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate

# Pick random candidate
execute as @n[tag=mgs.spawn_candidate,sort=random] run function mgs:v5.0.0/zombies/tp_to_spawn

# Cleanup
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

