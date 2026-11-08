
#> mgs:v5.4.1/multiplayer/custom/like_check_each
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/custom/like_modify_entry
#			mgs:v5.4.1/multiplayer/custom/like_check_each
#

execute store result score #liked_id mgs.data run data get storage mgs:temp _liked_iter[0].id
execute if score #liked_id mgs.data = #loadout_id mgs.data run scoreboard players set #already_liked mgs.data 1

data remove storage mgs:temp _liked_iter[0]
execute if data storage mgs:temp _liked_iter[0] unless score #already_liked mgs.data matches 1 run function mgs:v5.4.1/multiplayer/custom/like_check_each

