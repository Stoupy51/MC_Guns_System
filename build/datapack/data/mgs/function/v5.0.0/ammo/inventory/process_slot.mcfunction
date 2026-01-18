
#> mgs:v5.0.0/ammo/inventory/process_slot
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.0"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.1"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.2"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.3"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.4"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.5"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.6"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.7"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.8"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"weapon.offhand"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.0"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.1"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.2"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.3"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.4"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.5"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.6"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.7"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.8"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.9"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.10"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.11"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.12"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.13"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.14"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.15"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.16"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.17"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.18"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.19"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.20"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.21"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.22"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.23"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.24"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.25"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.26"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.27"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.28"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.29"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.30"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.31"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.32"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.33"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.34"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"container.35"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.cursor"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.0"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.1"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.2"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.3"}
#
# @args		slot (string)
#			base_weapon (unknown)
#

# Get bullets from the magazine
tag @s add mgs.extracting_bullets
execute summon item_display run function mgs:v5.0.0/ammo/extract_bullets {slot:"$(slot)"}
tag @s remove mgs.extracting_bullets
execute if score #bullets mgs.data matches 0 run return 0

# Calculate to_take = min(bullets, capacity - found_ammo)
scoreboard players operation #to_take mgs.data = #capacity mgs.data
scoreboard players operation #to_take mgs.data -= #found_ammo mgs.data
execute if score #bullets mgs.data < #to_take mgs.data run scoreboard players operation #to_take mgs.data = #bullets mgs.data

# Add to found_ammo
scoreboard players operation #found_ammo mgs.data += #to_take mgs.data

# Subtract from bullets
scoreboard players operation #bullets mgs.data -= #to_take mgs.data

# Modify the magazine item
$execute if score #bullets mgs.data matches ..0 run item modify entity @s $(slot) {function:"minecraft:set_components", components:{"minecraft:item_model":"$(base_weapon)_mag_empty"}}
execute store result storage mgs:temp magazine_bullets int 1 run scoreboard players get #bullets mgs.data
$item modify entity @s $(slot) mgs:v5.0.0/update_magazine_bullets

