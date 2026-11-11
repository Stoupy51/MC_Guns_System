
#> mgs:v5.4.2/multiplayer/custom/like_increment_rebuild
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/custom/like_increment_setup
#			mgs:v5.4.2/multiplayer/custom/like_increment_rebuild
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _like_src[0].id
execute if score #entry_id mgs.data = #loadout_id mgs.data run function mgs:v5.4.2/multiplayer/custom/like_increment_entry

data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _like_src[0]

data remove storage mgs:temp _like_src[0]
execute if data storage mgs:temp _like_src[0] run function mgs:v5.4.2/multiplayer/custom/like_increment_rebuild

