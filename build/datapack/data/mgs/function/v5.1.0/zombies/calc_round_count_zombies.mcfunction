
#> mgs:v5.1.0/zombies/calc_round_count_zombies
#
# @within	mgs:v5.1.0/zombies/start_round
#

scoreboard players operation #zb_to_spawn mgs.data = #zb_round mgs.data
scoreboard players add #zb_to_spawn mgs.data 7

# Rounds 1-9 run the eased ramp instead, meeting the formula above exactly at round 10
execute if score #zb_round mgs.data matches 1 run scoreboard players set #zb_to_spawn mgs.data 5
execute if score #zb_round mgs.data matches 2 run scoreboard players set #zb_to_spawn mgs.data 6
execute if score #zb_round mgs.data matches 3 run scoreboard players set #zb_to_spawn mgs.data 8
execute if score #zb_round mgs.data matches 4 run scoreboard players set #zb_to_spawn mgs.data 9
execute if score #zb_round mgs.data matches 5 run scoreboard players set #zb_to_spawn mgs.data 11
execute if score #zb_round mgs.data matches 6 run scoreboard players set #zb_to_spawn mgs.data 12
execute if score #zb_round mgs.data matches 7 run scoreboard players set #zb_to_spawn mgs.data 13
execute if score #zb_round mgs.data matches 8 run scoreboard players set #zb_to_spawn mgs.data 15
execute if score #zb_round mgs.data matches 9 run scoreboard players set #zb_to_spawn mgs.data 16
execute if score #zb_to_spawn mgs.data matches 97.. run scoreboard players set #zb_to_spawn mgs.data 96
scoreboard players operation #zb_to_spawn mgs.data *= #zb_player_count mgs.data
execute if score #zb_to_spawn mgs.data matches 257.. run scoreboard players set #zb_to_spawn mgs.data 256

## sourceMappingURL=calc_round_count_zombies.mcfunction.map
