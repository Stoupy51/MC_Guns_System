
#> mgs:v5.0.0/multiplayer/my_loadouts/check_private_not_fav
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/build_list_privates
#

execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 0 run function mgs:v5.0.0/multiplayer/shared/check_is_fav
execute if score #pub mgs.data matches 0 if score #is_fav mgs.data matches 0 run function mgs:v5.0.0/multiplayer/my_loadouts/prep_btn

