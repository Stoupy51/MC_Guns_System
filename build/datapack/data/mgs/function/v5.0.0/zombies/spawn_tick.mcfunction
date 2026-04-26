
#> mgs:v5.0.0/zombies/spawn_tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Decrease spawn timer
scoreboard players remove #zb_spawn_timer mgs.data 1
execute if score #zb_spawn_timer mgs.data matches 1.. run return 0

# Timer fired: recalculate timer and batch size for next cycle
function mgs:v5.0.0/zombies/calc_spawn_timer

# Spawn a batch of zombies (batch size depends on round)
scoreboard players operation #zb_spawn_batch_remaining mgs.data = #zb_spawn_batch mgs.data
function mgs:v5.0.0/zombies/spawn_batch_tick

