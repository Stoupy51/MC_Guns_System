
#> mgs:v5.4.0/ammo/inventory/set_item_model
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/ammo/inventory/process_slot {slot:"$(slot)",base_weapon:"$(base_weapon)"}
#
# @args		slot (string)
#			base_weapon (string)
#

$item modify entity @s $(slot) {type:"minecraft:set_components", components:{"minecraft:item_model":"mgs:$(base_weapon)_mag_empty"}}

