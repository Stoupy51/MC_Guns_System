
#> mgs:v5.0.0/zombies/glow_stuck_zombies
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Tag zombies currently within 32 blocks of any alive player
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.zombie_round,distance=..32] add mgs.zb_near_player

# Apply glowing for 6 seconds to zombies far from all players
effect give @e[tag=mgs.zombie_round,tag=!mgs.zb_near_player] glowing 6 0 true

# Cleanup temp tag
tag @e[tag=mgs.zb_near_player] remove mgs.zb_near_player

