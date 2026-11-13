
#> mgs:v5.4.2/zombies/save/rebuild_gun
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/rebuild_next with storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats
#
# @args		base_weapon (unknown)
#

item replace entity @n[type=minecraft:item_display,tag=mgs.sv_rebuild] contents with minecraft:air
$loot replace entity @n[type=minecraft:item_display,tag=mgs.sv_rebuild] contents loot mgs:i/$(base_weapon)
execute unless data entity @n[type=minecraft:item_display,tag=mgs.sv_rebuild] item run return 0
data modify storage mgs:temp _sv_fresh set from entity @n[type=minecraft:item_display,tag=mgs.sv_rebuild] item
data modify storage mgs:temp _sv_fresh.Slot set from storage mgs:temp _sv_item.Slot

execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.pap_level run function mgs:v5.4.2/zombies/save/rebuild_pap
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.remaining_bullets run data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats.remaining_bullets set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.remaining_bullets
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.fire_mode run data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats.fire_mode set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.fire_mode
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.models run data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats.models set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.models
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.scope_level run data modify storage mgs:temp _sv_fresh.components."minecraft:custom_data".mgs.stats.scope_level set from storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats.scope_level
data modify storage mgs:temp _sv_item set from storage mgs:temp _sv_fresh

