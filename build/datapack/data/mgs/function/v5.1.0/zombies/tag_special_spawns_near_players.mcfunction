
#> mgs:v5.1.0/zombies/tag_special_spawns_near_players
#
# @within	mgs:v5.1.0/zombies/spawn_dog
#

scoreboard players set #zb_near_found mgs.data 0

# First pass: 32 blocks from any alive player
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/tag_special_near_32

# Second pass: 64 blocks if none found
execute if score #zb_near_found mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/tag_special_near_64

# Fallback: any unlocked spawn. `store success` so #zb_near_found also reflects the fallback,
# letting callers gate "did we tag anything at all" purely on the score.
execute if score #zb_near_found mgs.data matches 0 store success score #zb_near_found mgs.data run tag @e[tag=mgs.spawn_special,tag=mgs.spawn_unlocked] add mgs.zb_near

