
#> mgs:v5.1.0/multiplayer/custom/fav_count_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/custom/fav_count_rebuild
#

execute unless data storage mgs:temp _fav_count_src[0].favorites_count run data modify storage mgs:temp _fav_count_src[0].favorites_count set value 0

execute store result score #fav_cnt mgs.data run data get storage mgs:temp _fav_count_src[0].favorites_count

execute if score #fav_found mgs.data matches 0 run scoreboard players add #fav_cnt mgs.data 1
execute if score #fav_found mgs.data matches 1 run scoreboard players remove #fav_cnt mgs.data 1

# Never below 0.
execute if score #fav_cnt mgs.data matches ..-1 run scoreboard players set #fav_cnt mgs.data 0

execute store result storage mgs:temp _fav_count_src[0].favorites_count int 1 run scoreboard players get #fav_cnt mgs.data

