
#> mgs:v5.0.0/ammo/inventory/has_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload with storage mgs:gun all.stats
#
# @args		base_weapon (unknown)
#

# Check all slots for matching magazines with bullets (return 1 if found, fail otherwise)
# Excludes empty non-consumable magazines (remaining_bullets: 0)
# Consumable magazines don't have this field, so they pass the 'unless' check if they exist
$execute if items entity @s hotbar.0 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.0 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.1 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.1 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.2 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.2 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.3 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.3 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.4 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.4 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.5 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.5 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.6 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.6 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.7 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.7 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s hotbar.8 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s hotbar.8 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s weapon.offhand *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s weapon.offhand *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.0 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.0 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.1 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.1 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.2 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.2 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.3 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.3 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.4 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.4 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.5 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.5 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.6 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.6 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.7 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.7 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.8 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.8 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.9 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.9 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.10 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.10 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.11 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.11 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.12 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.12 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.13 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.13 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.14 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.14 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.15 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.15 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.16 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.16 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.17 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.17 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.18 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.18 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.19 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.19 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.20 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.20 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.21 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.21 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.22 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.22 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.23 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.23 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.24 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.24 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.25 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.25 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s inventory.26 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s inventory.26 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.cursor *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s player.cursor *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.0 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s player.crafting.0 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.1 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s player.crafting.1 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.2 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s player.crafting.2 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.3 *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}}] unless items entity @s player.crafting.3 *[custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1

return fail

