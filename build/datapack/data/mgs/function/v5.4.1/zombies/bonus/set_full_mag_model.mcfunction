
#> mgs:v5.4.1/zombies/bonus/set_full_mag_model
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/bonus/refill_magazine with storage mgs:temp refill
#			mgs:v5.4.1/zombies/pap/upgrade_magazine_slot with storage mgs:temp refill
#
# @args		slot (unknown)
#			mag_model (unknown)
#			base_weapon (unknown)
#

$item modify entity @s $(slot) {"type":"minecraft:set_components", "components":{"minecraft:item_model":"$(mag_model)"}}

# A magazine that ran empty reads the empty model, so the full one is named from the weapon.
$execute if data storage mgs:temp refill{mag_model:"mgs:$(base_weapon)_mag_empty"} run item modify entity @s $(slot) {"type":"minecraft:set_components", "components":{"minecraft:item_model":"mgs:$(base_weapon)_mag"}}

