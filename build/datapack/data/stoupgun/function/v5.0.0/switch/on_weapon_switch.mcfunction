
#> stoupgun:v5.0.0/switch/on_weapon_switch
#
# @within	stoupgun:v5.0.0/switch/main
#

# Apply weapon switch cooldown only if it exceeds the current cooldown value
execute store result score #cooldown stoupgun.data run data get storage stoupgun:gun all.stats.switch
execute if score #cooldown stoupgun.data > @s stoupgun.cooldown run scoreboard players operation @s stoupgun.cooldown = #cooldown stoupgun.data

# When unequipping a weapon (player was holding a weapon):
#   - Find weapon with CURRENT_AMMO = -1 (needs update)
#   - Store current ammo count in weapon's stats
execute if score @s stoupgun.last_selected matches 1.. run function stoupgun:v5.0.0/ammo/update_old_weapon

# When equipping a new weapon:
#   - Load ammo count from weapon's stats into player scoreboard
#   - Mark weapon as needing update by setting ammo to -1
execute if score #current_id stoupgun.data matches 1.. run function stoupgun:v5.0.0/ammo/copy_data

