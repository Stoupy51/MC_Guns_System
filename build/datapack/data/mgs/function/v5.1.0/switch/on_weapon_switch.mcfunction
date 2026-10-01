
#> mgs:v5.1.0/switch/on_weapon_switch
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/main
#

# Deferred reload: no ammo was consumed yet.
execute if entity @s[tag=mgs.reloading] run tag @s remove mgs.reloading
execute if entity @s[tag=mgs.pump_sound] run tag @s remove mgs.pump_sound
execute if entity @s[tag=mgs.reload_mid_sound] run tag @s remove mgs.reload_mid_sound

# Zoomed on the previous weapon: clear the zoom score and slowness, or it stays stuck.
execute if score @s mgs.zoom matches 1 run function mgs:v5.1.0/zoom/clear_state

scoreboard players set @s mgs.burst_count 0

execute store result score #cooldown mgs.data run data get storage mgs:gun all.stats.switch

# quick_swap is a percentage (20 = 20% faster).
execute if score @s mgs.special.quick_swap matches 1.. run function mgs:v5.1.0/switch/apply_quick_swap

# As an expiry tick.
scoreboard players operation #cooldown mgs.data += #total_tick mgs.data
scoreboard players operation @s mgs.cooldown = #cooldown mgs.data

function mgs:v5.1.0/switch/force_switch_animation

function mgs:v5.1.0/ammo/compute_reserve

# Run as the player; weapon data in mgs:signals.
data modify storage mgs:signals on_switch set value {}
data modify storage mgs:signals on_switch.weapon set from storage mgs:gun all
function #mgs:signals/on_switch

# Unequipping: the previous weapon (remaining bullets -1) gets the player's ammo count back into its stats.
execute if score @s mgs.last_selected matches 1.. run function mgs:v5.1.0/ammo/update_old_weapon

# Equipping: its ammo count goes to the player's score, and the item is marked -1 (live in the score).
execute if score #current_id mgs.data matches 1.. run function mgs:v5.1.0/ammo/copy_data

