
#> mgs:v5.0.0/multiplayer/shared/check_is_fav
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/build_list_favs
#			mgs:v5.0.0/multiplayer/my_loadouts/check_private_not_fav
#			mgs:v5.0.0/multiplayer/my_loadouts/check_public_not_fav
#			mgs:v5.0.0/multiplayer/marketplace/build_list_favs
#			mgs:v5.0.0/multiplayer/marketplace/build_list_rest
#

execute store result score #check_id mgs.data run data get storage mgs:temp _iter[0].id
data modify storage mgs:temp _fav_check set from storage mgs:temp _cur_favorites
scoreboard players set #is_fav mgs.data 0
execute if data storage mgs:temp _fav_check[0] run function mgs:v5.0.0/multiplayer/shared/check_fav_iter

