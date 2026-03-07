
#> mgs:v5.0.0/multiplayer/pick_spawn_random
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/pick_spawn
#

execute as @n[tag=mgs.spawn_candidate,sort=random] run function mgs:v5.0.0/multiplayer/tp_to_spawn

# Clean up
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending
tag @a[tag=mgs.spawn_enemy] remove mgs.spawn_enemy

