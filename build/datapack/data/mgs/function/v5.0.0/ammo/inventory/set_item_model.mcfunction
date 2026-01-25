
#> mgs:v5.0.0/ammo/inventory/set_item_model
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/process_slot {slot:"$(slot)",base_weapon:"$(base_weapon)"}
#
# @args		slot (string)
#			base_weapon (unknown)
#

$item modify entity @s $(slot) {function:"minecraft:set_components", components:{"minecraft:item_model":"mgs:$(base_weapon)_mag_empty"}}

