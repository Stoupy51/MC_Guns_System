
#> mgs:v5.1.0/zombies/glow_stuck_zombies
#
# @within	mgs:v5.1.0/zombies/game_tick
#

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.zombie_round,distance=..32] add mgs.zb_near_player

effect give @e[tag=mgs.zombie_round,tag=!mgs.zb_near_player] glowing 6 0 true

tag @e[tag=mgs.zb_near_player] remove mgs.zb_near_player

