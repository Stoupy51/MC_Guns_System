
#> mgs:v5.0.0/zombies/inventory/fix_weapon_1
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots
#

# Search for a non-grenade gun in other hotbar slots and swap it back to hotbar.1
execute if items entity @s hotbar.0 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.0 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.0"}
execute if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.2 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.2"}
execute if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.3 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.3"}
execute if items entity @s hotbar.4 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.4 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.4"}
execute if items entity @s hotbar.5 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.5 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.5"}
execute if items entity @s hotbar.6 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.6 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.6"}
execute if items entity @s hotbar.8 *[custom_data~{mgs:{gun:true}}] unless items entity @s hotbar.8 *[custom_data~{mgs:{stats:{grenade_type:"frag"}}}] run return run function mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"hotbar.8"}

