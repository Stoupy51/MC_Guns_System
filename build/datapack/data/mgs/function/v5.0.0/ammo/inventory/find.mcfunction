
#> mgs:v5.0.0/ammo/inventory/find
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.stats
#
# @args		base_weapon (unknown)
#

# Get capacity and initialize found ammo to current remaining bullets
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute store result score #initial_ammo mgs.data run scoreboard players get @s mgs.remaining_bullets
scoreboard players operation #found_ammo mgs.data = #initial_ammo mgs.data

# Check all slots for magazines
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.0",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.1",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.2",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.3",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.4 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.4",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.5 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.5",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.6 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.6",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.7 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.7",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.8 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.8",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s weapon.offhand *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"weapon.offhand",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.0",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.1",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.2",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.3",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.4 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.4",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.5 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.5",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.6 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.6",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.7 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.7",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.8 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.8",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.9 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.9",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.10 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.10",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.11 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.11",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.12 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.12",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.13 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.13",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.14 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.14",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.15 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.15",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.16 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.16",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.17 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.17",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.18 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.18",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.19 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.19",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.20 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.20",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.21 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.21",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.22 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.22",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.23 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.23",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.24 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.24",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.25 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.25",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s inventory.26 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"inventory.26",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.cursor *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.cursor",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.0",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.1",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.2",base_weapon:"$(base_weapon)"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.3",base_weapon:"$(base_weapon)"}

# If found ammo, return success, else return fail
execute unless score @s mgs.remaining_bullets = #initial_ammo mgs.data run return 0
return fail

