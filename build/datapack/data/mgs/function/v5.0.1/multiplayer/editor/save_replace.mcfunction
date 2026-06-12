
#> mgs:v5.0.1/multiplayer/editor/save_replace
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/save
#

scoreboard players operation #edit_id mgs.data = @s mgs.mp.edit_target
data modify storage mgs:temp _edit_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
scoreboard players set #edit_replaced mgs.data 0
execute if data storage mgs:temp _edit_src[0] run function mgs:v5.0.1/multiplayer/editor/save_replace_iter

# If the original vanished in the meantime (e.g. deleted), append as a new entry
execute if score #edit_replaced mgs.data matches 0 run data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _new_loadout

