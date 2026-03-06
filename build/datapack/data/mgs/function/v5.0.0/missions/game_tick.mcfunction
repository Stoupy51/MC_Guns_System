
#> mgs:v5.0.0/missions/game_tick
#
# @within	mgs:v5.0.0/tick
#

# Boundary enforcement (skip players with respawn protection)
execute as @e[type=player,scores={mgs.mi.in_game=1,mgs.mp.death_count=0},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.0/missions/check_bounds

# OOB check
execute as @e[type=player,scores={mgs.mi.in_game=1,mgs.mp.death_count=0},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag=mgs.oob_point,distance=..5] run kill @s

# Check if all enemies are dead (level transition)
execute unless entity @e[tag=mgs.mission_enemy] if score #mi_level mgs.data matches 1..4 run function mgs:v5.0.0/missions/level_cleared

