
#> mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapon
#
# @within	mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.3"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.4"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.5"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.6"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.7"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"hotbar.8"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"weapon.offhand"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.3"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.4"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.5"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.6"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.7"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.8"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.9"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.10"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.11"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.12"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.13"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.14"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.15"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.16"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.17"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.18"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.19"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.20"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.21"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.22"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.23"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.24"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.25"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"inventory.26"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"player.cursor"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"player.crafting.0"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"player.crafting.1"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"player.crafting.2"}
#			mgs:v5.0.0/zombies/bonus/max_ammo_reload_all_weapons {slot:"player.crafting.3"}
#

# Set player's ammo count to weapon capacity
execute store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

