
#> mgs:v5.0.0/multiplayer/custom/like_check_each
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/like_modify_entry
#			mgs:v5.0.0/multiplayer/custom/like_check_each
#

execute store result score #liked_id mgs.data run data get storage mgs:temp _liked_iter[0].id
execute if score #liked_id mgs.data = #loadout_id mgs.data run scoreboard players set #already_liked mgs.data 1

data remove storage mgs:temp _liked_iter[0]
execute if data storage mgs:temp _liked_iter[0] unless score #already_liked mgs.data matches 1 run function mgs:v5.0.0/multiplayer/custom/like_check_each

