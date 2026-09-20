
#> mgs:v5.1.0/missions/death_watch_tick
#
# @within	mgs:v5.1.0/missions/game_tick
#

execute as @e[tag=mgs.mission_enemy,tag=!mgs.drop_done] at @s run function mgs:v5.1.0/missions/check_enemy_dead

