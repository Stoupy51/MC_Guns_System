
#> mgs:v5.4.2/multiplayer/custom/fav_check_each
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/custom/fav_modify_entry
#			mgs:v5.4.2/multiplayer/custom/fav_check_each
#

execute store result score #fav_id mgs.data run data get storage mgs:temp _fav_iter[0].id
execute if score #fav_id mgs.data = #loadout_id mgs.data run scoreboard players set #fav_found mgs.data 1

execute unless score #fav_id mgs.data = #loadout_id mgs.data run data modify storage mgs:temp _pd_src[0].favorites append from storage mgs:temp _fav_iter[0]

data remove storage mgs:temp _fav_iter[0]
execute if data storage mgs:temp _fav_iter[0] run function mgs:v5.4.2/multiplayer/custom/fav_check_each

