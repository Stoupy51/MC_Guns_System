
#> mgs:v5.1.0/zombies/calc_round_count_zombies
#
# @within	mgs:v5.1.0/zombies/start_round
#

scoreboard players operation #zb_to_spawn mgs.data = #zb_round mgs.data
scoreboard players add #zb_to_spawn mgs.data 7
execute if score #zb_to_spawn mgs.data matches 97.. run scoreboard players set #zb_to_spawn mgs.data 96
scoreboard players operation #zb_to_spawn mgs.data *= #zb_player_count mgs.data
execute if score #zb_to_spawn mgs.data matches 257.. run scoreboard players set #zb_to_spawn mgs.data 256

