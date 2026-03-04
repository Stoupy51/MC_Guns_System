
#> mgs:v5.0.0/multiplayer/marketplace/sort_build_list
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/browse_likes
#			mgs:v5.0.0/multiplayer/marketplace/sort_build_list
#

# Find max likes entry in _sort_pool
scoreboard players set #max_likes mgs.data -1
data modify storage mgs:temp _find_max_iter set from storage mgs:temp _sort_pool
execute if data storage mgs:temp _find_max_iter[0] run function mgs:v5.0.0/multiplayer/marketplace/sort_find_max

# Temporarily set _iter[0] to the best entry so prep_btn can use it
data modify storage mgs:temp _iter set value []
data modify storage mgs:temp _iter append from storage mgs:temp _sort_best
function mgs:v5.0.0/multiplayer/marketplace/prep_btn

# Remove best entry from _sort_pool (match by id)
execute store result score #extract_id mgs.data run data get storage mgs:temp _sort_best.id
data modify storage mgs:temp _pool_rebuild set from storage mgs:temp _sort_pool
data modify storage mgs:temp _sort_pool set value []
execute if data storage mgs:temp _pool_rebuild[0] run function mgs:v5.0.0/multiplayer/marketplace/sort_remove_best

# Recurse if pool still has entries
execute if data storage mgs:temp _sort_pool[0] run function mgs:v5.0.0/multiplayer/marketplace/sort_build_list

