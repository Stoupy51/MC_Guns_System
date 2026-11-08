
#> mgs:v5.4.1/maps/editor/summon_retry
#
# @within	mgs:v5.4.1/dialog/close_then
#			string in mgs:v5.4.1/maps/editor/summon_report
#

execute unless score @s mgs.mp.map_edit matches 1 run return fail
execute unless data storage mgs:temp map_edit{unsafe:1b} run return fail
scoreboard players set #ed_unloaded mgs.data 0
scoreboard players set #ed_retry mgs.data 1
data modify storage mgs:temp map_edit.missed_before set from storage mgs:temp map_edit.missed
data modify storage mgs:temp map_edit.missed set value []
function mgs:v5.4.1/maps/editor/summon_in with storage mgs:temp map_edit.force
scoreboard players set #ed_retry mgs.data 0
data remove storage mgs:temp map_edit.missed_before
function mgs:v5.4.1/maps/editor/summon_report
execute if score #ed_unloaded mgs.data matches 0 run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.every_element_is_loaded_saving_is_on","fallback":"Every element is loaded. Saving is on.","color":"green"}]

