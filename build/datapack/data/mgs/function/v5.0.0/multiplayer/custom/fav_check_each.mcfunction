
#> mgs:v5.0.0/multiplayer/custom/fav_check_each
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/fav_modify_entry
#			mgs:v5.0.0/multiplayer/custom/fav_check_each
#

# Check if this favorite's ID matches the target
execute store result score #fav_id mgs.data run data get storage mgs:temp _fav_iter[0].id
execute if score #fav_id mgs.data = #loadout_id mgs.data run scoreboard players set #fav_found mgs.data 1

# If not matching, keep it
execute unless score #fav_id mgs.data = #loadout_id mgs.data run data modify storage mgs:temp _pd_src[0].favorites append from storage mgs:temp _fav_iter[0]

# Next
data remove storage mgs:temp _fav_iter[0]
execute if data storage mgs:temp _fav_iter[0] run function mgs:v5.0.0/multiplayer/custom/fav_check_each

