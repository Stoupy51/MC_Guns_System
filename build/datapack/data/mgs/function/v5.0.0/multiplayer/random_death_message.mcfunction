
#> mgs:v5.0.0/multiplayer/random_death_message
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/multiplayer/simulate_death
#			mgs:v5.0.0/multiplayer/on_respawn
#

execute store result score #random_message mgs.data run random value 1..5
execute if score #random_message mgs.data matches 1 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"},{"translate": "mgs.made_a_terrible_mistake","color":"gray"}]
execute if score #random_message mgs.data matches 2 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"},{"translate": "mgs.forgot_how_gravity_works","color":"gray"}]
execute if score #random_message mgs.data matches 3 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"},{"translate": "mgs.played_themselves","color":"gray"}]
execute if score #random_message mgs.data matches 4 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"},{"translate": "mgs.left_the_battlefield","color":"gray"}]
execute if score #random_message mgs.data matches 5 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@s","color":"red"},{"translate": "mgs.embraced_the_void","color":"gray"}]

