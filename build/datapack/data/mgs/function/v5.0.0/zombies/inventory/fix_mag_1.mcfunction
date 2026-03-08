
#> mgs:v5.0.0/zombies/inventory/fix_mag_1
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots
#

execute if items entity @s hotbar.0 *[custom_data~{mgs:{magazine:true}}] run return run function mgs:v5.0.0/zombies/inventory/move_mag_to_inv1 {from:"hotbar.0"}
execute if items entity @s hotbar.1 *[custom_data~{mgs:{magazine:true}}] run return run function mgs:v5.0.0/zombies/inventory/move_mag_to_inv1 {from:"hotbar.1"}
execute if items entity @s hotbar.2 *[custom_data~{mgs:{magazine:true}}] run return run function mgs:v5.0.0/zombies/inventory/move_mag_to_inv1 {from:"hotbar.2"}
execute if items entity @s inventory.0 *[custom_data~{mgs:{magazine:true}}] run return run function mgs:v5.0.0/zombies/inventory/move_mag_to_inv1 {from:"inventory.0"}
execute if items entity @s inventory.2 *[custom_data~{mgs:{magazine:true}}] run return run function mgs:v5.0.0/zombies/inventory/move_mag_to_inv1 {from:"inventory.2"}

