
#> mgs:v5.0.0/multiplayer/marketplace/sort_find_max
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/sort_build_list
#			mgs:v5.0.0/multiplayer/marketplace/sort_find_max
#

execute unless data storage mgs:temp _find_max_iter[0].likes run data modify storage mgs:temp _find_max_iter[0].likes set value 0

execute store result score #this_likes mgs.data run data get storage mgs:temp _find_max_iter[0].likes
execute if score #this_likes mgs.data > #max_likes mgs.data run data modify storage mgs:temp _sort_best set from storage mgs:temp _find_max_iter[0]
execute if score #this_likes mgs.data > #max_likes mgs.data run scoreboard players operation #max_likes mgs.data = #this_likes mgs.data

data remove storage mgs:temp _find_max_iter[0]
execute if data storage mgs:temp _find_max_iter[0] run function mgs:v5.0.0/multiplayer/marketplace/sort_find_max

