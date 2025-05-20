
#> stoupgun:v5.0.0/switch/on_weapon_switch
#
# @within	stoupgun:v5.0.0/switch/main
#

# Set new weapon switch cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun all.stats.switch

# When unequipping a weapon (player was holding a weapon):
#   - Find weapon with CURRENT_AMMO = -1 (needs update)
#   - Store current ammo count in weapon's stats
execute if score @s stoupgun.last_selected matches 1.. run function stoupgun:v5.0.0/ammo/update_old_weapon

# When equipping a new weapon:
#   - Load ammo count from weapon's stats into player scoreboard
#   - Mark weapon as needing update by setting ammo to -1
execute if score #current_id stoupgun.data matches 1.. run function stoupgun:v5.0.0/ammo/copy_data

