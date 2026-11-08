
#> mgs:v5.4.1/multiplayer/custom/like_modify_entry
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/custom/like_pd_rebuild
#

data modify storage mgs:temp _liked_iter set from storage mgs:temp _pd_src[0].liked
execute if data storage mgs:temp _liked_iter[0] run function mgs:v5.4.1/multiplayer/custom/like_check_each

execute if score #already_liked mgs.data matches 0 run function mgs:v5.4.1/multiplayer/custom/like_append_new

