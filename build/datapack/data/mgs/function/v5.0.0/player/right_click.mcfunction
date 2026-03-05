
#> mgs:v5.0.0/player/right_click
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Block shooting during multiplayer prep phase
execute if data storage mgs:multiplayer game{state:"preparing"} if score @s mgs.mp.in_game matches 1 run return fail

# Decrease pending clicks by 1
scoreboard players remove @s mgs.pending_clicks 1

# If player stopped right clicking for 3 second, we update the item lore and reserve ammo
execute if score @s mgs.pending_clicks matches -60 if data storage mgs:gun all.gun run function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Stop here is weapon cooldown OR pending clicks if negative
execute if score @s mgs.cooldown matches 1.. run return fail
execute if score @s mgs.pending_clicks matches ..-1 run return fail

# Stop if SelectedItem is not a gun or if not enough ammo
execute unless data storage mgs:gun all.gun run return fail
execute unless score @s mgs.special.infinite_ammo matches 1.. if score @s mgs.remaining_bullets matches ..0 run return run function mgs:v5.0.0/ammo/reload

# Determine number of bullets to fire based on fire mode and held-click state
scoreboard players set #bullets_to_fire mgs.data 1

# Check fire mode
execute store result score #fire_mode_is_semi mgs.data if data storage mgs:gun all.stats{fire_mode:"semi"}
execute store result score #fire_mode_is_burst mgs.data if data storage mgs:gun all.stats{fire_mode:"burst"}

# Semi-auto mode: block if holding (only allow single taps)
execute if score #fire_mode_is_semi mgs.data matches 1 if score @s mgs.held_click matches 1.. run return fail

# Burst mode: check if burst limit reached, if so block firing
execute if score #fire_mode_is_burst mgs.data matches 1 store result score #burst_limit mgs.data run data get storage mgs:gun all.stats.burst
execute if score #fire_mode_is_burst mgs.data matches 1 if score @s mgs.burst_count >= #burst_limit mgs.data run return fail

# Burst mode: on first shot, set pending_clicks to (BURST-1) * COOLDOWN to sustain burst
execute if score #fire_mode_is_burst mgs.data matches 1 if score @s mgs.burst_count matches 0 run function mgs:v5.0.0/player/init_burst_clicks

# Burst mode: increment counter
execute if score #fire_mode_is_burst mgs.data matches 1 run scoreboard players add @s mgs.burst_count 1

# Auto mode: allow continuous fire (no blocking)

# Set cooldown (moved here from common.py so semi-auto check happens before cooldown is set)
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.cooldown

# Route to the appropriate firing method (projectile or hitscan)
function mgs:v5.0.0/player/fire_weapon

# Signal: on_shoot (weapon data available in mgs:signals)
data modify storage mgs:signals on_shoot set value {}
data modify storage mgs:signals on_shoot.weapon set from storage mgs:gun all
function #mgs:signals/on_shoot

# Simulate weapon kick
function mgs:v5.0.0/kicks/main

# Drop casing
function mgs:v5.0.0/casing/main

# Decrease bullet count
function mgs:v5.0.0/ammo/decrease

# Advanced Playsound
function mgs:v5.0.0/sound/main

