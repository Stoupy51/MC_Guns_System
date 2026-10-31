
#> mgs:v5.3.0/zombies/spawn_special_capped
#
# @within	mgs:v5.3.0/zombies/spawn_batch_tick
#

scoreboard players operation #zb_special_live mgs.data = #zb_alive mgs.data
scoreboard players operation #zb_special_live mgs.data += #zb_portal_pending mgs.data
execute if score #zb_special_live mgs.data >= #zb_special_cap mgs.data run return 0

function mgs:v5.3.0/zombies/spawn_from/special
execute if score #zb_spawned mgs.data matches 1 run scoreboard players remove #zb_to_spawn mgs.data 1

