
#> stoupgun:v5.0.0/ammo/update_old_weapon
#
# @within	stoupgun:v5.0.0/switch/on_weapon_switch
#

# Store the current bullet count from the player's scoreboard into the weapon's stats
execute store result storage stoupgun:temp remaining_bullets int 1 run scoreboard players get @s stoupgun.remaining_bullets

# For each slot, if remaining bullets is -1, update it
execute if items entity @s hotbar.0 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.0"}
execute if items entity @s hotbar.1 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.1"}
execute if items entity @s hotbar.2 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.2"}
execute if items entity @s hotbar.3 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.3"}
execute if items entity @s hotbar.4 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.4"}
execute if items entity @s hotbar.5 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.5"}
execute if items entity @s hotbar.6 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.6"}
execute if items entity @s hotbar.7 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.7"}
execute if items entity @s hotbar.8 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"hotbar.8"}
execute if items entity @s weapon.offhand *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"weapon.offhand"}
execute if items entity @s container.0 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.0"}
execute if items entity @s container.1 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.1"}
execute if items entity @s container.2 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.2"}
execute if items entity @s container.3 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.3"}
execute if items entity @s container.4 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.4"}
execute if items entity @s container.5 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.5"}
execute if items entity @s container.6 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.6"}
execute if items entity @s container.7 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.7"}
execute if items entity @s container.8 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.8"}
execute if items entity @s container.9 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.9"}
execute if items entity @s container.10 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.10"}
execute if items entity @s container.11 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.11"}
execute if items entity @s container.12 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.12"}
execute if items entity @s container.13 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.13"}
execute if items entity @s container.14 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.14"}
execute if items entity @s container.15 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.15"}
execute if items entity @s container.16 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.16"}
execute if items entity @s container.17 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.17"}
execute if items entity @s container.18 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.18"}
execute if items entity @s container.19 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.19"}
execute if items entity @s container.20 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.20"}
execute if items entity @s container.21 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.21"}
execute if items entity @s container.22 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.22"}
execute if items entity @s container.23 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.23"}
execute if items entity @s container.24 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.24"}
execute if items entity @s container.25 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.25"}
execute if items entity @s container.26 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.26"}
execute if items entity @s container.27 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.27"}
execute if items entity @s container.28 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.28"}
execute if items entity @s container.29 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.29"}
execute if items entity @s container.30 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.30"}
execute if items entity @s container.31 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.31"}
execute if items entity @s container.32 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.32"}
execute if items entity @s container.33 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.33"}
execute if items entity @s container.34 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.34"}
execute if items entity @s container.35 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"container.35"}
execute if items entity @s player.cursor *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"player.cursor"}
execute if items entity @s player.crafting.0 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"player.crafting.0"}
execute if items entity @s player.crafting.1 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"player.crafting.1"}
execute if items entity @s player.crafting.2 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"player.crafting.2"}
execute if items entity @s player.crafting.3 *[custom_data~{stoupgun:{stats:{remaining_bullets:-1}}}] run return run function stoupgun:v5.0.0/ammo/set_count {slot:"player.crafting.3"}

