
#> mgs:v5.0.0/multiplayer/shared/check_fav_iter
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/shared/check_is_fav
#			mgs:v5.0.0/multiplayer/shared/check_fav_iter
#

execute store result score #fav_entry_id mgs.data run data get storage mgs:temp _fav_check[0].id
execute if score #fav_entry_id mgs.data = #check_id mgs.data run scoreboard players set #is_fav mgs.data 1
data remove storage mgs:temp _fav_check[0]
execute unless score #is_fav mgs.data matches 1 if data storage mgs:temp _fav_check[0] run function mgs:v5.0.0/multiplayer/shared/check_fav_iter

