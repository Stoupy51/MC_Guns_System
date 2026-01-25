
#> mgs:v5.0.0/ammo/set_count
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.0"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.1"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.2"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.3"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.4"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.5"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.6"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.7"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"hotbar.8"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"weapon.offhand"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.0"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.1"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.2"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.3"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.4"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.5"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.6"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.7"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.8"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.9"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.10"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.11"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.12"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.13"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.14"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.15"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.16"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.17"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.18"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.19"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.20"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.21"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.22"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.23"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.24"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.25"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"inventory.26"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"player.cursor"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.0"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.1"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.2"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.3"}
#
# @args		slot (string)
#

# Apply new ammo count to weapon
$item modify entity @s $(slot) mgs:v5.0.0/update_ammo

# Update weapon's lore to show new ammo count
$function mgs:v5.0.0/ammo/modify_lore {slot:"$(slot)"}

