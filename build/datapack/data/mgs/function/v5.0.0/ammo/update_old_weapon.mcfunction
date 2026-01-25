
#> mgs:v5.0.0/ammo/update_old_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/on_weapon_switch
#

# Store player's current ammo count in temporary storage
execute store result storage mgs:temp remaining_bullets int 1 run scoreboard players get @s mgs.remaining_bullets

# Check all inventory slots for weapon needing ammo update (remaining bullets = -1)
execute if items entity @s hotbar.0 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.0"}
execute if items entity @s hotbar.1 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.1"}
execute if items entity @s hotbar.2 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.2"}
execute if items entity @s hotbar.3 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.3"}
execute if items entity @s hotbar.4 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.4"}
execute if items entity @s hotbar.5 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.5"}
execute if items entity @s hotbar.6 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.6"}
execute if items entity @s hotbar.7 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.7"}
execute if items entity @s hotbar.8 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"hotbar.8"}
execute if items entity @s weapon.offhand *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"weapon.offhand"}
execute if items entity @s inventory.0 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.0"}
execute if items entity @s inventory.1 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.1"}
execute if items entity @s inventory.2 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.2"}
execute if items entity @s inventory.3 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.3"}
execute if items entity @s inventory.4 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.4"}
execute if items entity @s inventory.5 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.5"}
execute if items entity @s inventory.6 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.6"}
execute if items entity @s inventory.7 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.7"}
execute if items entity @s inventory.8 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.8"}
execute if items entity @s inventory.9 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.9"}
execute if items entity @s inventory.10 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.10"}
execute if items entity @s inventory.11 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.11"}
execute if items entity @s inventory.12 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.12"}
execute if items entity @s inventory.13 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.13"}
execute if items entity @s inventory.14 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.14"}
execute if items entity @s inventory.15 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.15"}
execute if items entity @s inventory.16 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.16"}
execute if items entity @s inventory.17 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.17"}
execute if items entity @s inventory.18 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.18"}
execute if items entity @s inventory.19 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.19"}
execute if items entity @s inventory.20 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.20"}
execute if items entity @s inventory.21 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.21"}
execute if items entity @s inventory.22 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.22"}
execute if items entity @s inventory.23 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.23"}
execute if items entity @s inventory.24 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.24"}
execute if items entity @s inventory.25 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.25"}
execute if items entity @s inventory.26 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"inventory.26"}
execute if items entity @s player.cursor *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"player.cursor"}
execute if items entity @s player.crafting.0 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"player.crafting.0"}
execute if items entity @s player.crafting.1 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"player.crafting.1"}
execute if items entity @s player.crafting.2 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"player.crafting.2"}
execute if items entity @s player.crafting.3 *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.0.0/ammo/set_count {slot:"player.crafting.3"}

