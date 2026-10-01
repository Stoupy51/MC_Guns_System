
#> mgs:v5.1.0/zombies/pick_spawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/tp_all_to_spawns [ at @s ]
#			mgs:v5.1.0/zombies/respawn_tp
#

tag @s add mgs.spawn_pending

# Unused spawns; `store success` says whether any was tagged, so the "all used" fallback tests a score instead of scanning @e.
execute store success score #has_candidate mgs.data run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked,tag=!mgs.spawn_used] add mgs.spawn_candidate

# All used: every spawn is a candidate again.
execute if score #has_candidate mgs.data matches 0 run tag @e[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate

execute as @n[tag=mgs.spawn_candidate,sort=random] run function mgs:v5.1.0/shared/tp_to_spawn {mode:"zombies"}

tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

