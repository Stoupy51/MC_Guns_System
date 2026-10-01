
#> mgs:v5.1.0/missions/spawn_all_enemies
#
# @within	mgs:v5.1.0/missions/end_prep
#

data modify storage mgs:temp _enemy_iter set from storage mgs:missions game.map.enemies

execute if data storage mgs:temp _enemy_iter[0] run function mgs:v5.1.0/missions/spawn_enemy_iter

execute as @e[tag=mgs.armed,tag=!mgs.mission_enemy] run tag @s add mgs.mission_enemy
execute as @e[tag=mgs.mission_enemy] run tag @s add mgs.gm_entity
team join mgs.mi_mobs @e[tag=mgs.mission_enemy]

execute store result score #mi_total_enemies mgs.data if entity @e[tag=mgs.mission_enemy]

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"score":{"name":"#mi_total_enemies","objective":"mgs.data"},"color":"yellow"}," ",{"translate":"mgs.enemies_spawned","color":"gray"}]

