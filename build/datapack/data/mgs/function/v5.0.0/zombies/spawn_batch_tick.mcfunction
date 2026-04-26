
#> mgs:v5.0.0/zombies/spawn_batch_tick
#
# @within	mgs:v5.0.0/zombies/spawn_tick
#			mgs:v5.0.0/zombies/spawn_batch_tick
#

# Guard: nothing left to spawn
execute if score #zb_to_spawn mgs.data matches ..0 run return 0

# Spawn one zombie
function mgs:v5.0.0/zombies/spawn_zombie
scoreboard players remove #zb_to_spawn mgs.data 1
scoreboard players remove #zb_spawn_batch_remaining mgs.data 1

# Recurse if batch not exhausted and zombies remain
execute if score #zb_spawn_batch_remaining mgs.data matches 1.. if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.0.0/zombies/spawn_batch_tick

