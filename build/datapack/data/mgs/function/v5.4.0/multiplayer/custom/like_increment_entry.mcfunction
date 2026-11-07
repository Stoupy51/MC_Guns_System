
#> mgs:v5.4.0/multiplayer/custom/like_increment_entry
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/custom/like_increment_rebuild
#

# Older entries may have no likes field.
execute unless data storage mgs:temp _like_src[0].likes run data modify storage mgs:temp _like_src[0].likes set value 0
execute store result score #likes mgs.data run data get storage mgs:temp _like_src[0].likes
scoreboard players add #likes mgs.data 1
execute store result storage mgs:temp _like_src[0].likes int 1 run scoreboard players get #likes mgs.data

