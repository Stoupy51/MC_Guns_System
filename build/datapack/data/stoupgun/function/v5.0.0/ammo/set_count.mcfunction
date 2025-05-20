
#> stoupgun:v5.0.0/ammo/set_count
#
# @within	stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.0"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.1"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.2"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.3"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.4"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.5"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.6"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.7"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"hotbar.8"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"weapon.offhand"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.0"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.1"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.2"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.3"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.4"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.5"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.6"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.7"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.8"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.9"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.10"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.11"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.12"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.13"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.14"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.15"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.16"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.17"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.18"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.19"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.20"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.21"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.22"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.23"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.24"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.25"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.26"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.27"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.28"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.29"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.30"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.31"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.32"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.33"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.34"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"container.35"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"player.cursor"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.0"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.1"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.2"}
#			stoupgun:v5.0.0/ammo/update_old_weapon {slot:"player.crafting.3"}
#

# Item modifier to apply the new remaining bullets count
$item modify entity @s $(slot) stoupgun:v5.0.0/update_ammo

# Modify gun lore
function stoupgun:v5.0.0/ammo/modify_lore {slot:"$(slot)"}

