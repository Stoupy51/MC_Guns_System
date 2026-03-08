
#> mgs:v5.0.0/zombies/spawn_tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Decrease spawn timer
scoreboard players remove #zb_spawn_timer mgs.data 1
execute if score #zb_spawn_timer mgs.data matches 1.. run return 0

# Reset timer (spawn every 1 second)
scoreboard players set #zb_spawn_timer mgs.data 20

# Spawn a zombie
function mgs:v5.0.0/zombies/spawn_zombie

# Decrease count to spawn
scoreboard players remove #zb_to_spawn mgs.data 1

