
#> mgs:v5.4.2/multiplayer/marketplace/build_list_favs
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/marketplace/browse
#			mgs:v5.4.2/multiplayer/marketplace/browse_fav_only
#			mgs:v5.4.2/multiplayer/marketplace/build_list_favs
#

execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 1 run function mgs:v5.4.2/multiplayer/shared/check_is_fav
execute if score #pub mgs.data matches 1 if score #is_fav mgs.data matches 1 run function mgs:v5.4.2/multiplayer/marketplace/prep_btn

data remove storage mgs:temp _iter[0]
execute if data storage mgs:temp _iter[0] run function mgs:v5.4.2/multiplayer/marketplace/build_list_favs

