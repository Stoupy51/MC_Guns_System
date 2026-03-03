
#> mgs:v5.0.0/multiplayer/custom/toggle_vis_rebuild
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/toggle_visibility
#			mgs:v5.0.0/multiplayer/custom/toggle_vis_rebuild
#

# Check if this entry matches our target (ID + ownership)
execute store result score #entry_id mgs.data run data get storage mgs:temp _del_src[0].id
execute store result score #entry_owner mgs.data run data get storage mgs:temp _del_src[0].owner_pid
scoreboard players set #vis_match mgs.data 0
execute if score #entry_id mgs.data = #loadout_id mgs.data if score #entry_owner mgs.data = @s mgs.mp.pid run scoreboard players set #vis_match mgs.data 1

# If this is the target, toggle its public flag
execute if score #vis_match mgs.data matches 1 run function mgs:v5.0.0/multiplayer/custom/toggle_entry_vis

# Append entry (possibly toggled)
data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _del_src[0]

data remove storage mgs:temp _del_src[0]
execute if data storage mgs:temp _del_src[0] run function mgs:v5.0.0/multiplayer/custom/toggle_vis_rebuild

