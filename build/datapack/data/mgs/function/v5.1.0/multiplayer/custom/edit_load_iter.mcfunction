
#> mgs:v5.1.0/multiplayer/custom/edit_load_iter
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/custom/edit
#			mgs:v5.1.0/multiplayer/custom/edit_load_iter
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _find_iter[0].id
execute if score #entry_id mgs.data = #loadout_id mgs.data if data storage mgs:temp _find_iter[0].editor_state run data modify storage mgs:temp editor set from storage mgs:temp _find_iter[0].editor_state
execute if score #entry_id mgs.data = #loadout_id mgs.data if data storage mgs:temp _find_iter[0].editor_state run scoreboard players set #edit_found mgs.data 1
execute if score #entry_id mgs.data = #loadout_id mgs.data run return 0

# Not found yet, continue search
data remove storage mgs:temp _find_iter[0]
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.1.0/multiplayer/custom/edit_load_iter

