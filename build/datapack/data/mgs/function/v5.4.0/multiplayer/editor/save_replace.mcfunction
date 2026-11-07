
#> mgs:v5.4.0/multiplayer/editor/save_replace
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/save
#

scoreboard players operation #edit_id mgs.data = @s mgs.mp.edit_target
data modify storage mgs:temp _edit_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
scoreboard players set #edit_replaced mgs.data 0
execute if data storage mgs:temp _edit_src[0] run function mgs:v5.4.0/multiplayer/editor/save_replace_iter

# The original was deleted meanwhile: append as new.
execute if score #edit_replaced mgs.data matches 0 run data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _new_loadout

