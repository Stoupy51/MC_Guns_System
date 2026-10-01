
#> mgs:v5.1.0/zombies/spawn_batch_tick
#
# @within	mgs:v5.1.0/zombies/spawn_tick
#			mgs:v5.1.0/zombies/spawn_batch_tick
#

execute if score #zb_to_spawn mgs.data matches ..0 run return 0

# Dog rounds release one hound per timer tick, capped by how many are out.
execute if score #zb_dog_round mgs.data matches 1 run return run function mgs:v5.1.0/zombies/spawn_dog_capped

function mgs:v5.1.0/zombies/spawn_zombie
scoreboard players remove #zb_to_spawn mgs.data 1
scoreboard players remove #zb_spawn_batch_remaining mgs.data 1

execute if score #zb_spawn_batch_remaining mgs.data matches 1.. if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.1.0/zombies/spawn_batch_tick

