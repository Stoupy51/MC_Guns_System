
#> mgs:v5.3.0/multiplayer/random_self_kill_message
#
# @executed	at @s
#
# @within	mgs:v5.3.0/multiplayer/simulate_death_fire_kill
#

execute store result score #random_message mgs.data run random value 1..5
execute if score #random_message mgs.data matches 1 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.blew_themselves_up","fallback":"blew themselves up","color":"gray"}]
execute if score #random_message mgs.data matches 2 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.got_a_taste_of_their_own_medicine","fallback":"got a taste of their own medicine","color":"gray"}]
execute if score #random_message mgs.data matches 3 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.found_out_the_blast_radius_the_hard_way","fallback":"found out the blast radius the hard way","color":"gray"}]
execute if score #random_message mgs.data matches 4 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.didnt_throw_the_grenade_far_enough","fallback":"didn't throw the grenade far enough","color":"gray"}]
execute if score #random_message mgs.data matches 5 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.is_their_own_worst_enemy","fallback":"is their own worst enemy","color":"gray"}]

