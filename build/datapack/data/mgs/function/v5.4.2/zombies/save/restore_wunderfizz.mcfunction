
#> mgs:v5.4.2/zombies/save/restore_wunderfizz
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/restore
#

execute store result score #sv_id mgs.data run data get storage mgs:zombies_saves loading.map.wunderfizz
scoreboard players set #sv_found mgs.data 0
execute as @e[tag=mgs.wunderfizz_machine] if score @s mgs.zb.wf.id = #sv_id mgs.data run scoreboard players set #sv_found mgs.data 1
execute if score #sv_found mgs.data matches 0 run return run data modify storage mgs:temp _sv_missing append value {element:"wunderfizz"}

tag @e[tag=mgs.wf_active] remove mgs.wf_active
execute as @e[tag=mgs.wunderfizz_machine] if score @s mgs.zb.wf.id = #sv_id mgs.data run tag @s add mgs.wf_active
function mgs:v5.4.2/zombies/wunderfizz/sync_displays
function mgs:v5.4.2/zombies/wunderfizz/sync_visibility

