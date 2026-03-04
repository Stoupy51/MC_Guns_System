
#> mgs:v5.0.0/multiplayer/shared/load_player_favorites
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/browse
#			mgs:v5.0.0/multiplayer/my_loadouts/browse_fav_only
#			mgs:v5.0.0/multiplayer/marketplace/browse
#			mgs:v5.0.0/multiplayer/marketplace/browse_fav_only
#			mgs:v5.0.0/multiplayer/marketplace/browse_likes
#

# Default to empty favorites
data modify storage mgs:temp _cur_favorites set value []
# Scan player_data for our PID entry and copy its favorites list
data modify storage mgs:temp _pd_iter set from storage mgs:multiplayer player_data
execute if data storage mgs:temp _pd_iter[0] run function mgs:v5.0.0/multiplayer/shared/load_fav_iter

