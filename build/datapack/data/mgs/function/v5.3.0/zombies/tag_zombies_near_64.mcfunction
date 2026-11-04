
#> mgs:v5.3.0/zombies/tag_zombies_near_64
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/tag_zombies_spawns_near_players [ at @s ]
#

execute store result score #zb_px mgs.data run data get entity @s Pos[0] 10
execute store result score #zb_py mgs.data run data get entity @s Pos[1] 10
execute store result score #zb_pz mgs.data run data get entity @s Pos[2] 10
tag @e[type=minecraft:marker,tag=mgs.spawn_unlocked,tag=mgs.spawn_round_ok,tag=mgs.spawn_powered,tag=mgs.spawn_abox_ok,tag=mgs.spawn_zb,distance=..64] add mgs.zb_cand
execute as @e[type=minecraft:marker,tag=mgs.zb_cand] run function mgs:v5.3.0/zombies/near_within_64
tag @e[type=minecraft:marker,tag=mgs.zb_cand] remove mgs.zb_cand
execute store result score #zb_near_found mgs.data if entity @e[type=minecraft:marker,tag=mgs.zb_near]

