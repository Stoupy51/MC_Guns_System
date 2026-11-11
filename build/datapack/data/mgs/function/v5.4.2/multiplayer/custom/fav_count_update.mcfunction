
#> mgs:v5.4.2/multiplayer/custom/fav_count_update
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/custom/toggle_favorite
#

data modify storage mgs:temp _fav_count_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _fav_count_src[0] run function mgs:v5.4.2/multiplayer/custom/fav_count_rebuild

