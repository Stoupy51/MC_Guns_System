
#> mgs:v5.1.0/zombies/calc_spawn_timer
#
# @within	mgs:v5.1.0/zombies/start_round
#			mgs:v5.1.0/zombies/spawn_tick
#

scoreboard players set #zb_spawn_timer mgs.data 20
scoreboard players operation #zb_spawn_timer mgs.data -= #zb_round mgs.data
execute if score #zb_spawn_timer mgs.data matches ..1 run scoreboard players set #zb_spawn_timer mgs.data 1

scoreboard players operation #zb_spawn_batch mgs.data = #zb_round mgs.data
scoreboard players remove #zb_spawn_batch mgs.data 1
scoreboard players operation #zb_spawn_batch mgs.data /= #50 mgs.data
scoreboard players add #zb_spawn_batch mgs.data 1

# Dog rounds pace on the concurrency cap of spawn_dog_capped, not on the zombie curve,
# which reaches 1 tick by round 20 and would release a whole pack in one second.
execute if score #zb_dog_round mgs.data matches 1 run scoreboard players set #zb_spawn_timer mgs.data 20
execute if score #zb_dog_round mgs.data matches 1 run scoreboard players set #zb_spawn_batch mgs.data 1

