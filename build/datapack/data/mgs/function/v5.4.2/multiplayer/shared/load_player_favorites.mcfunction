
#> mgs:v5.4.2/multiplayer/shared/load_player_favorites
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/my_loadouts/browse
#			mgs:v5.4.2/multiplayer/my_loadouts/browse_fav_only
#			mgs:v5.4.2/multiplayer/marketplace/browse
#			mgs:v5.4.2/multiplayer/marketplace/browse_fav_only
#			mgs:v5.4.2/multiplayer/marketplace/browse_likes
#

data modify storage mgs:temp _cur_favorites set value []
data modify storage mgs:temp _pd_iter set from storage mgs:multiplayer player_data
execute if data storage mgs:temp _pd_iter[0] run function mgs:v5.4.2/multiplayer/shared/load_fav_iter

