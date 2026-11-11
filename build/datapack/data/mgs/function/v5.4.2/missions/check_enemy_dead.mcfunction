
#> mgs:v5.4.2/missions/check_enemy_dead
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/death_watch_tick [ as @e[tag=...] & at @s ]
#

scoreboard players set #mi_enemy_hp mgs.data 1000
execute store result score #mi_enemy_hp mgs.data run data get entity @s Health 100
execute if score #mi_enemy_hp mgs.data matches ..0 run function mgs:v5.4.2/missions/drop_enemy_weapon

