
#> mgs:v5.0.0/multiplayer/custom/like_increment_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/like_increment_rebuild
#

# Ensure likes field exists, then increment
execute unless data storage mgs:temp _like_src[0].likes run data modify storage mgs:temp _like_src[0].likes set value 0
execute store result score #likes mgs.data run data get storage mgs:temp _like_src[0].likes
scoreboard players add #likes mgs.data 1
execute store result storage mgs:temp _like_src[0].likes int 1 run scoreboard players get #likes mgs.data

