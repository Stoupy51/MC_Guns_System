
#> mgs:v5.4.0/multiplayer/custom/like_increment_setup
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/custom/like
#

data modify storage mgs:temp _like_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _like_src[0] run function mgs:v5.4.0/multiplayer/custom/like_increment_rebuild

