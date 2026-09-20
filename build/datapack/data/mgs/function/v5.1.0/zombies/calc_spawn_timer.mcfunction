
#> mgs:v5.1.0/zombies/calc_spawn_timer
#
# @within	mgs:v5.1.0/zombies/start_round
#			mgs:v5.1.0/zombies/spawn_tick
#

# Timer: start at 20, clamp to minimum 1
scoreboard players set #zb_spawn_timer mgs.data 20
scoreboard players operation #zb_spawn_timer mgs.data -= #zb_round mgs.data
execute if score #zb_spawn_timer mgs.data matches ..1 run scoreboard players set #zb_spawn_timer mgs.data 1

# Batch: (round - 1) / 50 + 1
scoreboard players operation #zb_spawn_batch mgs.data = #zb_round mgs.data
scoreboard players remove #zb_spawn_batch mgs.data 1
scoreboard players operation #zb_spawn_batch mgs.data /= #50 mgs.data
scoreboard players add #zb_spawn_batch mgs.data 1

# Dog rounds ignore the zombie curve entirely: flat 1s between hounds, with the concurrency cap in
# spawn_dog_capped doing the real pacing. The zombie formula bottoms out at 1 tick / batch 2 by
# round 20, which dumped a whole pack in a single second.
execute if score #zb_dog_round mgs.data matches 1 run scoreboard players set #zb_spawn_timer mgs.data 20
execute if score #zb_dog_round mgs.data matches 1 run scoreboard players set #zb_spawn_batch mgs.data 1

