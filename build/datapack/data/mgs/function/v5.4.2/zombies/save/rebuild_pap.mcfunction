
#> mgs:v5.4.2/zombies/save/rebuild_pap
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/rebuild_gun
#

data modify storage mgs:temp _pap_extract set value {}
data modify storage mgs:temp _pap_extract.stats set from storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats
execute store result score #pap_next_idx mgs.data run data get storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.pap_level
scoreboard players remove #pap_next_idx mgs.data 1
function mgs:v5.4.2/zombies/pap/apply_runtime_overrides
data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats set from storage mgs:temp _pap_extract.stats
data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats.pap_level set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.pap_level
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.weapon run data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.weapon set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.weapon
data modify storage mgs:temp _sv_fresh.components."minecraft:item_name" set from storage mgs:temp _sv_item.components."minecraft:item_name"
data modify storage mgs:temp _sv_fresh.components."minecraft:lore" set from storage mgs:temp _sv_item.components."minecraft:lore"
data modify storage mgs:temp _sv_fresh.components."minecraft:item_model" set from storage mgs:temp _sv_item.components."minecraft:item_model"

