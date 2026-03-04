
#> mgs:v5.0.0/multiplayer/custom/fav_count_rebuild
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/fav_count_update
#			mgs:v5.0.0/multiplayer/custom/fav_count_rebuild
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _fav_count_src[0].id
execute if score #entry_id mgs.data = #loadout_id mgs.data run function mgs:v5.0.0/multiplayer/custom/fav_count_entry

data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _fav_count_src[0]

data remove storage mgs:temp _fav_count_src[0]
execute if data storage mgs:temp _fav_count_src[0] run function mgs:v5.0.0/multiplayer/custom/fav_count_rebuild

