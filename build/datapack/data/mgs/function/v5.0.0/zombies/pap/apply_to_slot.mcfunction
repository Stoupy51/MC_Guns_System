
#> mgs:v5.0.0/zombies/pap/apply_to_slot
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap
#
# @args		slot (unknown)
#

$item modify entity @s $(slot) mgs:v5.0.0/zb_pap_apply_stats
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_apply_name.slot set value "$(slot)"
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_apply_name.name set from storage mgs:temp _pap_extract.new_name
execute if data storage mgs:temp _pap_extract.new_name run function mgs:v5.0.0/zombies/pap/set_item_name with storage mgs:temp _pap_apply_name
execute if data storage mgs:temp _pap_extract.lore[0] run data modify storage mgs:temp _pap_apply_lore.slot set value "$(slot)"
execute if data storage mgs:temp _pap_extract.lore[0] run data modify storage mgs:temp _pap_apply_lore.lore set from storage mgs:temp _pap_extract.lore
execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.0.0/zombies/pap/set_item_lore with storage mgs:temp _pap_apply_lore
$function mgs:v5.0.0/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}

