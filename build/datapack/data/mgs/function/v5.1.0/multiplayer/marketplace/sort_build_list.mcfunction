
#> mgs:v5.1.0/multiplayer/marketplace/sort_build_list
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/marketplace/browse_likes
#			mgs:v5.1.0/multiplayer/marketplace/sort_build_list
#

scoreboard players set #max_likes mgs.data -1
data modify storage mgs:temp _find_max_iter set from storage mgs:temp _sort_pool
execute if data storage mgs:temp _find_max_iter[0] run function mgs:v5.1.0/multiplayer/marketplace/sort_find_max

# prep_btn reads _iter[0].
data modify storage mgs:temp _iter set value []
data modify storage mgs:temp _iter append from storage mgs:temp _sort_best
function mgs:v5.1.0/multiplayer/marketplace/prep_btn

# Matched by id.
execute store result score #extract_id mgs.data run data get storage mgs:temp _sort_best.id
data modify storage mgs:temp _pool_rebuild set from storage mgs:temp _sort_pool
data modify storage mgs:temp _sort_pool set value []
execute if data storage mgs:temp _pool_rebuild[0] run function mgs:v5.1.0/multiplayer/marketplace/sort_remove_best

execute if data storage mgs:temp _sort_pool[0] run function mgs:v5.1.0/multiplayer/marketplace/sort_build_list

