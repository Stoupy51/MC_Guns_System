
#> mgs:v5.0.0/ammo/inventory/find
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload run return fail
#
# @args		base_weapon (unknown)
#

# Get capacity and initialize found ammo
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
scoreboard players set #found_ammo mgs.data 0

# Check all slots for magazines
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.0"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.1"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.2"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.3"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.4 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.4"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.5 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.5"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.6 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.6"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.7 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.7"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s hotbar.8 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"hotbar.8"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s weapon.offhand *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"weapon.offhand"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.0"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.1"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.2"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.3"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.4 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.4"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.5 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.5"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.6 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.6"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.7 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.7"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.8 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.8"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.9 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.9"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.10 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.10"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.11 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.11"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.12 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.12"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.13 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.13"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.14 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.14"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.15 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.15"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.16 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.16"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.17 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.17"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.18 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.18"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.19 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.19"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.20 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.20"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.21 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.21"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.22 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.22"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.23 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.23"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.24 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.24"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.25 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.25"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.26 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.26"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.27 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.27"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.28 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.28"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.29 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.29"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.30 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.30"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.31 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.31"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.32 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.32"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.33 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.33"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.34 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.34"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s container.35 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"container.35"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.cursor *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.cursor"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.0 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.0"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.1 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.1"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.2 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.2"}
$execute if score #found_ammo mgs.data < #capacity mgs.data if items entity @s player.crafting.3 *[custom_data~{mgs:{"magazine":true,"weapon":"$(base_weapon)"}}] run function mgs:v5.0.0/ammo/inventory/process_slot {slot:"player.crafting.3"}

# If found ammo, set remaining bullets and return success
execute if score #found_ammo mgs.data matches 1.. run return run scoreboard players operation @s mgs.remaining_bullets = #found_ammo mgs.data

# No ammo found, return fail
return fail

