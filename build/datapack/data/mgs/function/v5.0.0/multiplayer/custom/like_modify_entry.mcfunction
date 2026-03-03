
#> mgs:v5.0.0/multiplayer/custom/like_modify_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/like_pd_rebuild
#

# Iterate liked[] to check if already liked
data modify storage mgs:temp _liked_iter set from storage mgs:temp _pd_src[0].liked
execute if data storage mgs:temp _liked_iter[0] run function mgs:v5.0.0/multiplayer/custom/like_check_each

# If not already liked, add to liked[] list
execute if score #already_liked mgs.data matches 0 run function mgs:v5.0.0/multiplayer/custom/like_append_new

