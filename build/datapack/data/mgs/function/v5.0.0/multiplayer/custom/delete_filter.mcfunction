
#> mgs:v5.0.0/multiplayer/custom/delete_filter
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/delete
#			mgs:v5.0.0/multiplayer/custom/delete_filter
#

# Check if this entry matches BOTH the target ID and our PID
execute store result score #entry_id mgs.data run data get storage mgs:temp _del_src[0].id
execute store result score #entry_owner mgs.data run data get storage mgs:temp _del_src[0].owner_pid
scoreboard players set #del_match mgs.data 0
execute if score #entry_id mgs.data = #loadout_id mgs.data if score #entry_owner mgs.data = @s mgs.mp.pid run scoreboard players set #del_match mgs.data 1

# If NOT a delete match, keep the entry
execute unless score #del_match mgs.data matches 1 run data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _del_src[0]

# Next
data remove storage mgs:temp _del_src[0]
execute if data storage mgs:temp _del_src[0] run function mgs:v5.0.0/multiplayer/custom/delete_filter

