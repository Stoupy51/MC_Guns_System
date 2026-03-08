
#> mgs:v5.0.0/zombies/inventory/move_mag_to_inv1
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/fix_mag_1 {from:"hotbar.0"}
#			mgs:v5.0.0/zombies/inventory/fix_mag_1 {from:"hotbar.1"}
#			mgs:v5.0.0/zombies/inventory/fix_mag_1 {from:"hotbar.2"}
#			mgs:v5.0.0/zombies/inventory/fix_mag_1 {from:"inventory.0"}
#			mgs:v5.0.0/zombies/inventory/fix_mag_1 {from:"inventory.2"}
#
# @args		from (string)
#

$item replace entity @s inventory.1 from entity @s $(from)
$item replace entity @s $(from) with air

