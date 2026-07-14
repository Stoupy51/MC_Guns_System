
#> mgs:v5.1.0/multiplayer/editor/save_replace_iter
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/save_replace
#			mgs:v5.1.0/multiplayer/editor/save_replace_iter
#

# Match by id + ownership
execute store result score #entry_id mgs.data run data get storage mgs:temp _edit_src[0].id
execute store result score #entry_owner mgs.data run data get storage mgs:temp _edit_src[0].owner_pid
scoreboard players set #edit_match mgs.data 0
execute if score #entry_id mgs.data = #edit_id mgs.data if score #entry_owner mgs.data = @s mgs.mp.pid run scoreboard players set #edit_match mgs.data 1

# On match: carry over social stats, then insert the rebuilt loadout in place of the original
execute if score #edit_match mgs.data matches 1 if data storage mgs:temp _edit_src[0].likes run data modify storage mgs:temp _new_loadout.likes set from storage mgs:temp _edit_src[0].likes
execute if score #edit_match mgs.data matches 1 if data storage mgs:temp _edit_src[0].favorites_count run data modify storage mgs:temp _new_loadout.favorites_count set from storage mgs:temp _edit_src[0].favorites_count
execute if score #edit_match mgs.data matches 1 run data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _new_loadout
execute if score #edit_match mgs.data matches 1 run scoreboard players set #edit_replaced mgs.data 1
execute unless score #edit_match mgs.data matches 1 run data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _edit_src[0]

data remove storage mgs:temp _edit_src[0]
execute if data storage mgs:temp _edit_src[0] run function mgs:v5.1.0/multiplayer/editor/save_replace_iter

