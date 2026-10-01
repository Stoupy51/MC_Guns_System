
#> mgs:v5.1.0/zombies/spawn_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

scoreboard players remove #zb_spawn_timer mgs.data 1
execute if score #zb_spawn_timer mgs.data matches 1.. run return 0

function mgs:v5.1.0/zombies/calc_spawn_timer

scoreboard players operation #zb_spawn_batch_remaining mgs.data = #zb_spawn_batch mgs.data
function mgs:v5.1.0/zombies/spawn_batch_tick

