
#> mgs:v5.0.0/switch/on_weapon_switch
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/main
#

# If player was reloading, cancel reload (deferred: no ammo consumed yet)
execute if entity @s[tag=mgs.reloading] run tag @s remove mgs.reloading
execute if entity @s[tag=mgs.pump_sound] run tag @s remove mgs.pump_sound
execute if entity @s[tag=mgs.reload_mid_sound] run tag @s remove mgs.reload_mid_sound

# Apply weapon switch cooldown from stats
execute store result score #cooldown mgs.data run data get storage mgs:gun all.stats.switch

# Apply quick swap: reduce cooldown by quick_swap% (e.g. 20 = 20% faster)
execute if score @s mgs.special.quick_swap matches 1.. run function mgs:v5.0.0/switch/apply_quick_swap

# Convert to expiration tick and set as both cooldown and switch_cooldown
scoreboard players operation #cooldown mgs.data += #total_tick mgs.data
scoreboard players operation @s mgs.cooldown = #cooldown mgs.data

# Mirror into switch_cooldown (used by shader zoom guard, unaffected by shooting)
scoreboard players operation @s mgs.switch_cooldown = #cooldown mgs.data

# Force weapon switch animation
function mgs:v5.0.0/switch/force_switch_animation

# Recompute reserve ammo for the newly equipped weapon
function mgs:v5.0.0/ammo/compute_reserve

# Signal: on_switch (@s = player, weapon data in mgs:signals)
data modify storage mgs:signals on_switch set value {}
data modify storage mgs:signals on_switch.weapon set from storage mgs:gun all
function #mgs:signals/on_switch

# When unequipping a weapon (player was holding a weapon):
#   - Find weapon with CURRENT_AMMO = -1 (needs update)
#   - Store current ammo count in weapon's stats
execute if score @s mgs.last_selected matches 1.. run function mgs:v5.0.0/ammo/update_old_weapon

# When equipping a new weapon:
#   - Load ammo count from weapon's stats into player scoreboard
#   - Mark weapon as needing update by setting ammo to -1
execute if score #current_id mgs.data matches 1.. run function mgs:v5.0.0/ammo/copy_data

