
#> mgs:v5.4.0/zombies/aura_tick
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/game_tick [ at @s ]
#

effect give @e[type=minecraft:zombie,tag=mgs.zombie_round,distance=..6] minecraft:resistance 2 1 true
particle minecraft:soul_fire_flame ~ ~1 ~ 3.0 0.5 3.0 0 12 normal

