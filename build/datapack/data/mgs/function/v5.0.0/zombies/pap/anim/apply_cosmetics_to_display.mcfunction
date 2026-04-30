
#> mgs:v5.0.0/zombies/pap/anim/apply_cosmetics_to_display
#
# @executed	as @n[tag=mgs.pap_weapon_display,distance=..2]
#
# @within	mgs:v5.0.0/zombies/pap/anim/apply_cosmetics [ as @n[tag=mgs.pap_weapon_display,distance=..2] ]
#

data modify entity @s item.components."minecraft:custom_data".mgs.stats.models set from storage mgs:temp _pap_pending_cosmetics.models
data remove entity @s item.components."minecraft:custom_data".mgs.weapon
execute if data storage mgs:temp _pap_pending_cosmetics.weapon run data modify entity @s item.components."minecraft:custom_data".mgs.weapon set from storage mgs:temp _pap_pending_cosmetics.weapon
data remove entity @s item.components."minecraft:custom_data".mgs.stats.scope_level
execute if data storage mgs:temp _pap_pending_cosmetics.scope_level run data modify entity @s item.components."minecraft:custom_data".mgs.stats.scope_level set from storage mgs:temp _pap_pending_cosmetics.scope_level
data modify storage mgs:temp _pap_scope_model.slot set value "contents"
data modify storage mgs:temp _pap_scope_model.model set from storage mgs:temp _pap_pending_cosmetics.models.normal
function mgs:v5.0.0/zombies/pap/set_item_model_from_scope with storage mgs:temp _pap_scope_model

