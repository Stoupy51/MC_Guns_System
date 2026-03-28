
#> mgs:v5.0.0/missions/game_tick
#
# @within	mgs:v5.0.0/tick
#

# Spectate Timer (3s respawn cooldown)
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players remove @s mgs.mp.spectate_timer 1
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=40},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_2_seconds","color":"gray"}]
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=20},gamemode=spectator] run title @s subtitle [{"translate":"mgs.respawning_in_1_second","color":"gray"}]
execute as @a[scores={mgs.mi.in_game=1,mgs.mp.spectate_timer=0},gamemode=spectator] at @s run function mgs:v5.0.0/missions/actual_respawn

# Increment mission timer
scoreboard players add #mi_timer mgs.data 1

# Boundary enforcement (skip spectators) & OOB Check
execute as @e[tag=mgs.mission_enemy] at @s run function mgs:v5.0.0/missions/check_bounds
execute as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.0/missions/check_bounds
execute as @e[type=player,scores={mgs.mi.in_game=1},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag=mgs.oob_point,distance=..5] run damage @s 10000 out_of_world

# Track enemy kills (total enemies - alive enemies)
execute store result score #alive mgs.data if entity @e[tag=mgs.mission_enemy]
scoreboard players operation #mi_kills mgs.data = #mi_total_enemies mgs.data
scoreboard players operation #mi_kills mgs.data -= #alive mgs.data

# Update compass for all players (point to nearest enemy)
execute as @a[scores={mgs.mi.in_game=1}] at @s run function mgs:v5.0.0/missions/update_compass
execute at @r[scores={mgs.mi.in_game=1}] run kill @e[type=experience_orb,distance=..200]

# Check if all enemies are dead → victory
execute unless entity @e[tag=mgs.mission_enemy] run return run function mgs:v5.0.0/missions/victory

