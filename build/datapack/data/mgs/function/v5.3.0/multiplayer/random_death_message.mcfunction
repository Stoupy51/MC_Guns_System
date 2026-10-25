
#> mgs:v5.3.0/multiplayer/random_death_message
#
# @executed	at @s
#
# @within	mgs:v5.3.0/multiplayer/simulate_death
#			mgs:v5.3.0/multiplayer/on_respawn
#

execute store result score #random_message mgs.data run random value 1..5
execute if score #random_message mgs.data matches 1 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.made_a_terrible_mistake","fallback":"made a terrible mistake","color":"gray"}]
execute if score #random_message mgs.data matches 2 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.forgot_how_gravity_works","fallback":"forgot how gravity works","color":"gray"}]
execute if score #random_message mgs.data matches 3 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.played_themselves","fallback":"played themselves","color":"gray"}]
execute if score #random_message mgs.data matches 4 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.left_the_battlefield","fallback":"left the battlefield","color":"gray"}]
execute if score #random_message mgs.data matches 5 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s"}]," ",{"translate":"mgs.embraced_the_void","fallback":"embraced the void","color":"gray"}]

