
#> mgs:v5.0.0/ammo/reserve/extract_slot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.0"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.1"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.2"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.3"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.4"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.5"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.6"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.7"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"hotbar.8"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"weapon.offhand"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.0"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.1"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.2"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.3"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.4"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.5"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.6"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.7"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.8"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.9"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.10"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.11"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.12"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.13"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.14"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.15"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.16"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.17"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.18"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.19"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.20"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.21"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.22"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.23"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.24"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.25"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"inventory.26"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"player.cursor"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"player.crafting.0"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"player.crafting.1"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"player.crafting.2"}
#			mgs:v5.0.0/ammo/reserve/scan {slot:"player.crafting.3"}
#
# @args		slot (string)
#

# Called for each slot containing a matching magazine
# Spawn temp entity to read item data
tag @s add mgs.reading_reserve
$execute summon item_display run function mgs:v5.0.0/ammo/reserve/read_item {slot:"$(slot)"}
tag @s remove mgs.reading_reserve

