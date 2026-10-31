
#> mgs:v5.3.0/zombies/tag_special_near_32
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/tag_special_spawns_near_players [ at @s ]
#

execute store result score #zb_near_hit mgs.data run tag @e[type=minecraft:marker,tag=mgs.spawn_unlocked,tag=mgs.spawn_round_ok,tag=mgs.spawn_powered,tag=mgs.spawn_abox_ok,tag=mgs.spawn_special,distance=..32] add mgs.zb_near
scoreboard players operation #zb_near_found mgs.data += #zb_near_hit mgs.data

