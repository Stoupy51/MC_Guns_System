
#> mgs:v5.4.2/multiplayer/custom/fav_modify_entry
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/custom/fav_pd_rebuild
#

data modify storage mgs:temp _fav_iter set from storage mgs:temp _pd_src[0].favorites
data modify storage mgs:temp _pd_src[0].favorites set value []

# Remove it if present.
execute if data storage mgs:temp _fav_iter[0] run function mgs:v5.4.2/multiplayer/custom/fav_check_each

# Not present: add it.
execute if score #fav_found mgs.data matches 0 run function mgs:v5.4.2/multiplayer/custom/fav_append_new

