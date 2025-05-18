
#> stoupgun:v5.0.0/switch/on_weapon_switch
#
# @within	stoupgun:v5.0.0/switch/main
#

# Set new weapon switch cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun stats.switch

# 1. When unequipping a weapon (`if score @s stoupgun.last_selected matches 1..` means player was holding a weapon)
#   - Find the weapon with CURRENT_AMMO set to -1 (meaning not updated)
#   - Set the score @s stoupgun.remaining_bullets into this weapon's stats.remaining_bullets
execute if score @s stoupgun.last_selected matches 1.. run function stoupgun:v5.0.0/ammo/update_old_weapon

# 2. When equipping a weapon (current weapon id):
#   - Copy stats.remaining_bullets into @s stoupgun.remaining_bullets
#   - Set stats.remaining_bullets to -1 (indicating it needs to be updated)
execute if score #current_id stoupgun.data matches 1.. run function stoupgun:v5.0.0/ammo/copy_data

