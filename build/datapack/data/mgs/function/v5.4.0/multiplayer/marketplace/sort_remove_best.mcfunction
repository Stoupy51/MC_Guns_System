
#> mgs:v5.4.0/multiplayer/marketplace/sort_remove_best
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/marketplace/sort_build_list
#			mgs:v5.4.0/multiplayer/marketplace/sort_remove_best
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _pool_rebuild[0].id
execute unless score #entry_id mgs.data = #extract_id mgs.data run data modify storage mgs:temp _sort_pool append from storage mgs:temp _pool_rebuild[0]

data remove storage mgs:temp _pool_rebuild[0]
execute if data storage mgs:temp _pool_rebuild[0] run function mgs:v5.4.0/multiplayer/marketplace/sort_remove_best

