
#> mgs:v5.4.1/multiplayer/marketplace/sort_collect_pool
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/marketplace/browse_likes
#			mgs:v5.4.1/multiplayer/marketplace/sort_collect_pool
#

execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 1 run data modify storage mgs:temp _sort_pool append from storage mgs:temp _iter[0]

data remove storage mgs:temp _iter[0]
execute if data storage mgs:temp _iter[0] run function mgs:v5.4.1/multiplayer/marketplace/sort_collect_pool

