
#> mgs:v5.0.0/zombies/inventory/swap_to_1
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.0"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.2"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.3"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.4"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.5"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.6"}
#			mgs:v5.0.0/zombies/inventory/fix_weapon_1 {from:"hotbar.8"}
#
# @args		from (string)
#

tag @s add mgs.inv_fix
$execute summon item_display run function mgs:v5.0.0/zombies/inventory/do_swap_1 {from:"$(from)"}
tag @s remove mgs.inv_fix

