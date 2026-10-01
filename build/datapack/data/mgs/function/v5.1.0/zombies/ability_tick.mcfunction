
#> mgs:v5.1.0/zombies/ability_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Coward: below half health, teleport to a spawn (1-round cooldown).
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability=1,mgs.zb.ability_cd=0},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/perks/check_coward

