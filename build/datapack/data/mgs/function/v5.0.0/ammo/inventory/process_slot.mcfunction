
#> mgs:v5.0.0/ammo/inventory/process_slot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.0",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.1",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.2",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.3",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.4",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.5",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.6",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.7",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"hotbar.8",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"weapon.offhand",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.0",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.1",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.2",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.3",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.4",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.5",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.6",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.7",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.8",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.9",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.10",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.11",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.12",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.13",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.14",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.15",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.16",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.17",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.18",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.19",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.20",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.21",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.22",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.23",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.24",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.25",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"inventory.26",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.cursor",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.0",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.1",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.2",base_weapon:"$(base_weapon)"}
#			mgs:v5.0.0/ammo/inventory/find {slot:"player.crafting.3",base_weapon:"$(base_weapon)"}
#
# @args		slot (string)
#			base_weapon (unknown)
#

# Get bullets from the magazine
tag @s add mgs.extracting_bullets
$execute summon item_display run function mgs:v5.0.0/ammo/extract_bullets {slot:"$(slot)"}
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
$execute if score #bullets mgs.data matches ..0 run function mgs:v5.0.0/ammo/inventory/set_item_model {slot:"$(slot)",base_weapon:"$(base_weapon)"}
execute store result storage mgs:temp remaining_bullets int 1 run scoreboard players get #bullets mgs.data
$item modify entity @s $(slot) mgs:v5.0.0/update_ammo

# Update magazine lore
$function mgs:v5.0.0/ammo/modify_mag_lore {slot:"$(slot)"}

# Update player's ammo count
scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

