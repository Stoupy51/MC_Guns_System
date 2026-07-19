
#> mgs:v5.1.0/zombies/tag_special_near_32
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/tag_special_spawns_near_players [ at @s ]
#

execute store result score #zb_near_hit mgs.data run tag @e[tag=mgs.spawn_special,tag=mgs.spawn_unlocked,distance=..32] add mgs.zb_near
scoreboard players operation #zb_near_found mgs.data += #zb_near_hit mgs.data

