
#> mgs:v5.1.0/multiplayer/custom/fav_modify_entry
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/custom/fav_pd_rebuild
#

data modify storage mgs:temp _fav_iter set from storage mgs:temp _pd_src[0].favorites
data modify storage mgs:temp _pd_src[0].favorites set value []

# Remove it if present.
execute if data storage mgs:temp _fav_iter[0] run function mgs:v5.1.0/multiplayer/custom/fav_check_each

# Not present: add it.
execute if score #fav_found mgs.data matches 0 run function mgs:v5.1.0/multiplayer/custom/fav_append_new

