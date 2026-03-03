
#> mgs:v5.0.0/multiplayer/custom/fav_modify_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/fav_pd_rebuild
#

# Copy favorites for iteration, clear them for rebuild
data modify storage mgs:temp _fav_iter set from storage mgs:temp _pd_src[0].favorites
data modify storage mgs:temp _pd_src[0].favorites set value []

# Iterate favorites to remove if found
execute if data storage mgs:temp _fav_iter[0] run function mgs:v5.0.0/multiplayer/custom/fav_check_each

# If not found (wasn't in favorites), add it
execute if score #fav_found mgs.data matches 0 run function mgs:v5.0.0/multiplayer/custom/fav_append_new

