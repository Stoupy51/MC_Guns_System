
#> mgs:v5.0.0/ammo/set_count
#
# @executed	as @a[sort=random] & at @s
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
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.0"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.1"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.2"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.3"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.4"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.5"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.6"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.7"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.8"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.9"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.10"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.11"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.12"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.13"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.14"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.15"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.16"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.17"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.18"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.19"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.20"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.21"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.22"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.23"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.24"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.25"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.26"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.27"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.28"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.29"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.30"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.31"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.32"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.33"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.34"}
#			mgs:v5.0.0/ammo/update_old_weapon {slot:"container.35"}
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

