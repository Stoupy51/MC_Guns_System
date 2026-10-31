
#> mgs:v5.3.0/zombies/spawn_batch_tick
#
# @within	mgs:v5.3.0/zombies/spawn_tick
#			mgs:v5.3.0/zombies/spawn_batch_tick
#

execute if score #zb_to_spawn mgs.data matches ..0 run return 0

# Special rounds release one enemy per timer tick, capped by how many are out.
execute if score #zb_special_round mgs.data matches 1 run return run function mgs:v5.3.0/zombies/spawn_special_capped

# With no open spawn the enemy stays queued, and the watchdog ends a round that never gets one.
function mgs:v5.3.0/zombies/spawn_from/zombies
execute if score #zb_spawned mgs.data matches 0 run return 0
scoreboard players remove #zb_to_spawn mgs.data 1
scoreboard players remove #zb_spawn_batch_remaining mgs.data 1

execute if score #zb_spawn_batch_remaining mgs.data matches 1.. if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.3.0/zombies/spawn_batch_tick

