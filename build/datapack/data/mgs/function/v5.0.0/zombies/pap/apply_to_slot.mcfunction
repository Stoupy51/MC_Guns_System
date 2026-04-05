
#> mgs:v5.0.0/zombies/pap/apply_to_slot
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap
#
# @args		slot (unknown)
#

$item modify entity @s $(slot) mgs:v5.0.0/zb_pap_apply_stats
$data modify storage mgs:temp _pap_name_data.slot set value "$(slot)"
function mgs:v5.0.0/zombies/pap/set_item_name_with_level with storage mgs:temp _pap_name_data
$execute if data storage mgs:temp _pap_extract.lore[0] run data modify storage mgs:temp _pap_apply_lore.slot set value "$(slot)"
execute if data storage mgs:temp _pap_extract.lore[0] run data modify storage mgs:temp _pap_apply_lore.lore set from storage mgs:temp _pap_extract.lore
execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.0.0/zombies/pap/set_item_lore with storage mgs:temp _pap_apply_lore

# Set enchantment glint on PAP weapons
$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:enchantment_glint_override":true}}

# Update item_model to match new scope
$data modify storage mgs:temp _pap_scope_model.slot set value "$(slot)"
data modify storage mgs:temp _pap_scope_model.model set from storage mgs:temp _pap_extract.stats.models.normal
function mgs:v5.0.0/zombies/pap/set_item_model_from_scope with storage mgs:temp _pap_scope_model

$function mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}

