
#> mgs:v5.0.0/zombies/bonus/set_full_mag_model
#
# @within	mgs:v5.0.0/zombies/bonus/refill_magazine with storage mgs:temp refill
#
# @args		slot (unknown)
#			base_weapon (unknown)
#

$item modify entity @s $(slot) {"function":"minecraft:set_components", "components":{"minecraft:item_model":"mgs:$(base_weapon)_mag"}}

