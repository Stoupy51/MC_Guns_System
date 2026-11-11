
#> mgs:v5.4.2/zombies/tag_special_spawns_near_players
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/on_stuck_zombie
#			mgs:v5.4.2/zombies/spawn_from/special
#

scoreboard players set #zb_near_found mgs.data 0

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.4.2/zombies/tag_special_near_32

execute if score #zb_near_found mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.4.2/zombies/tag_special_near_64

# `store success` so #zb_near_found also reflects the fallback.
execute if score #zb_near_found mgs.data matches 0 store success score #zb_near_found mgs.data run tag @e[type=minecraft:marker,tag=mgs.spawn_unlocked,tag=mgs.spawn_round_ok,tag=mgs.spawn_powered,tag=mgs.spawn_abox_ok,tag=mgs.spawn_special] add mgs.zb_near

