
#> mgs:v5.4.2/missions/death_watch_tick
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/game_tick
#

execute as @e[tag=mgs.mission_enemy,tag=!mgs.drop_done] at @s run function mgs:v5.4.2/missions/check_enemy_dead

