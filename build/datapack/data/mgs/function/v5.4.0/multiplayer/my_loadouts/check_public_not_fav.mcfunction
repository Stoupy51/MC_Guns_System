
#> mgs:v5.4.0/multiplayer/my_loadouts/check_public_not_fav
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/my_loadouts/build_list_publics
#

execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 1 run function mgs:v5.4.0/multiplayer/shared/check_is_fav
execute if score #pub mgs.data matches 1 if score #is_fav mgs.data matches 0 run function mgs:v5.4.0/multiplayer/my_loadouts/prep_btn

