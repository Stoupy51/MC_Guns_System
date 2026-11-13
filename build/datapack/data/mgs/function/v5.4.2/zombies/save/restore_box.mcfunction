
#> mgs:v5.4.2/zombies/save/restore_box
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/restore
#

execute store result score #sv_id mgs.data run data get storage mgs:zombies_saves loading.map.box
scoreboard players set #sv_found mgs.data 0
execute as @e[tag=mgs.mystery_box_pos] if score @s mgs.mb.box = #sv_id mgs.data run scoreboard players set #sv_found mgs.data 1
execute if score #sv_found mgs.data matches 0 run return run data modify storage mgs:temp _sv_missing append value {element:"box"}

tag @e[tag=mgs.mystery_box_active] remove mgs.mystery_box_active
execute as @e[tag=mgs.mystery_box_pos] if score @s mgs.mb.box = #sv_id mgs.data run tag @s add mgs.mystery_box_active
function mgs:v5.4.2/zombies/mystery_box/sync_presence_display
function mgs:v5.4.2/zombies/mystery_box/sync_interaction_visibility

