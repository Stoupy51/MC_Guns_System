
#> mgs:v5.1.0/multiplayer/random_kill_message
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/simulate_death_fire_kill
#			mgs:v5.1.0/multiplayer/on_respawn
#

execute store result score #random_message mgs.data run random value 1..5
execute if score #random_message mgs.data matches 1 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@a[tag=mgs.temp_killer]"}," ",{"translate":"mgs.eliminated","color":"gray"}," ",{"selector":"@a[tag=mgs.temp_victim]"}]
execute if score #random_message mgs.data matches 2 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@a[tag=mgs.temp_killer]"}," ",{"translate":"mgs.took_down","color":"gray"}," ",{"selector":"@a[tag=mgs.temp_victim]"}]
execute if score #random_message mgs.data matches 3 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@a[tag=mgs.temp_killer]"}," ",{"translate":"mgs.dispatched","color":"gray"}," ",{"selector":"@a[tag=mgs.temp_victim]"}]
execute if score #random_message mgs.data matches 4 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@a[tag=mgs.temp_killer]"}," ",{"translate":"mgs.sent","color":"gray"}," ",{"selector":"@a[tag=mgs.temp_victim]"}," ",{"translate":"mgs.to_the_shadow_realm","color":"gray"}]
execute if score #random_message mgs.data matches 5 run tellraw @a[scores={mgs.mp.in_game=1..}] ["",{"selector":"@a[tag=mgs.temp_killer]"}," ",{"translate":"mgs.wiped","color":"gray"}," ",{"selector":"@a[tag=mgs.temp_victim]"}," ",{"translate":"mgs.off_the_map","color":"gray"}]

