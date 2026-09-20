
#> mgs:v5.1.0/zombies/spawn_dog_capped
#
# @within	mgs:v5.1.0/zombies/spawn_batch_tick
#

scoreboard players operation #zb_dog_live mgs.data = #zb_alive mgs.data
scoreboard players operation #zb_dog_live mgs.data += #zb_dog_pending mgs.data
execute if score #zb_dog_live mgs.data >= #zb_dog_cap mgs.data run return 0

function mgs:v5.1.0/zombies/spawn_dog
scoreboard players remove #zb_to_spawn mgs.data 1

