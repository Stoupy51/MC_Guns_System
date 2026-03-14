
#> mgs:v5.0.0/multiplayer/random_self_kill_message
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/multiplayer/simulate_death_fire_kill
#

execute store result score #random_message mgs.data run random value 1..5
execute if score #random_message mgs.data matches 1 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"}," ",{"translate":"mgs.blew_themselves_up","color":"gray"}]
execute if score #random_message mgs.data matches 2 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"}," ",{"translate":"mgs.got_a_taste_of_their_own_medicine","color":"gray"}]
execute if score #random_message mgs.data matches 3 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"}," ",{"translate":"mgs.found_out_the_blast_radius_the_hard_way","color":"gray"}]
execute if score #random_message mgs.data matches 4 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"}," ",{"translate":"mgs.didnt_throw_the_grenade_far_enough","color":"gray"}]
execute if score #random_message mgs.data matches 5 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"}," ",{"translate":"mgs.is_their_own_worst_enemy","color":"gray"}]

