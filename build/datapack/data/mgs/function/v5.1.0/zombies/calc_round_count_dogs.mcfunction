
#> mgs:v5.1.0/zombies/calc_round_count_dogs
#
# @within	mgs:v5.1.0/zombies/start_round
#

scoreboard players operation #zb_to_spawn mgs.data = #zb_round mgs.data
scoreboard players operation #zb_to_spawn mgs.data /= #3 mgs.data
scoreboard players add #zb_to_spawn mgs.data 4
execute if score #zb_to_spawn mgs.data matches 13.. run scoreboard players set #zb_to_spawn mgs.data 12
scoreboard players operation #zb_to_spawn mgs.data *= #zb_player_count mgs.data
execute if score #zb_to_spawn mgs.data matches 49.. run scoreboard players set #zb_to_spawn mgs.data 48

# Hounds come in packs scaled by players (solo 3, 4 players 6), refilled as they die (BO).
scoreboard players operation #zb_dog_cap mgs.data = #zb_player_count mgs.data
scoreboard players add #zb_dog_cap mgs.data 2

# The guaranteed Max Ammo of this round.
scoreboard players set #zb_dog_ammo_done mgs.data 0

