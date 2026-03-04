
#> mgs:v5.0.0/multiplayer/custom/fav_count_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/fav_count_rebuild
#

# Ensure favorites_count field exists
execute unless data storage mgs:temp _fav_count_src[0].favorites_count run data modify storage mgs:temp _fav_count_src[0].favorites_count set value 0

# Load current count into score
execute store result score #fav_cnt mgs.data run data get storage mgs:temp _fav_count_src[0].favorites_count

# fav_found=0 means just added → increment; fav_found=1 means just removed → decrement
execute if score #fav_found mgs.data matches 0 run scoreboard players add #fav_cnt mgs.data 1
execute if score #fav_found mgs.data matches 1 run scoreboard players remove #fav_cnt mgs.data 1

# Clamp to 0 minimum
execute if score #fav_cnt mgs.data matches ..-1 run scoreboard players set #fav_cnt mgs.data 0

# Store back
execute store result storage mgs:temp _fav_count_src[0].favorites_count int 1 run scoreboard players get #fav_cnt mgs.data

