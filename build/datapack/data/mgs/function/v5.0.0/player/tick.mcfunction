
#> mgs:v5.0.0/player/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/tick [ as @e[type=player,sort=random] & at @s ]
#

# Custom loadouts: assign player ID if not yet assigned
execute unless score @s mgs.mp.pid matches 1.. run function mgs:v5.0.0/multiplayer/assign_pid

# Add temporary tag
tag @s add mgs.ticking

# Compute acoustics (#TODO: Only if player moved enough, and every second not tick)
function mgs:v5.0.0/sound/compute_acoustics

# Change mode if weapon is in offhand
execute if items entity @s weapon.offhand * run function mgs:v5.0.0/player/mode_check

# Check if player dropped weapon to reload
function mgs:v5.0.0/switch/check_reload_on_drop

# Copy gun data
function mgs:v5.0.0/utils/copy_gun_data

# Check if we need to zoom weapon or stop
function mgs:v5.0.0/zoom/main

# Check if switching weapon
function mgs:v5.0.0/switch/main

# Decrease cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# Decrease switch_cooldown by 1 (separate from shooting cooldown)
execute if score @s mgs.switch_cooldown matches 1.. run scoreboard players remove @s mgs.switch_cooldown 1

# Check mid cooldown sound
execute if score @s mgs.cooldown matches 1.. if entity @s[tag=mgs.pump_sound] if data storage mgs:gun all.sounds.pump run function mgs:v5.0.0/sound/check/pump
execute if score @s mgs.cooldown matches 0 if entity @s[tag=mgs.pump_sound] run tag @s remove mgs.pump_sound

# Check mid reload sound
execute if score @s mgs.cooldown matches 1.. if entity @s[tag=mgs.reload_mid_sound] if data storage mgs:gun all.sounds.playermid run function mgs:v5.0.0/sound/check/reload_mid
execute if score @s mgs.cooldown matches 0 if entity @s[tag=mgs.reload_mid_sound] run tag @s remove mgs.reload_mid_sound

# Check if we need to play reload end sound
execute if score @s mgs.cooldown matches 1.. if data storage mgs:gun all.sounds.playerend run function mgs:v5.0.0/sound/check/reload_end
execute if score @s mgs.cooldown matches 0 if entity @s[tag=mgs.reloading] run function mgs:v5.0.0/ammo/end_reload

# If pending clicks, run right click function
execute if score @s mgs.pending_clicks matches -100.. run function mgs:v5.0.0/player/right_click

# Reset held_click when player stops holding (pending_clicks goes negative)
execute if score @s mgs.pending_clicks matches ..-1 run scoreboard players set @s mgs.held_click 0

# Reset burst_count only if burst completed or player switched weapons
execute if score @s mgs.pending_clicks matches ..-1 run function mgs:v5.0.0/player/reset_burst_if_complete

# Show action bar
execute if data storage mgs:gun all.gun run function mgs:v5.0.0/actionbar/show

# DPS timer: every 20 ticks snapshot mgs.dps -> mgs.previous_dps and reset
scoreboard players add @s mgs.dps_timer 1
execute if score @s mgs.dps_timer matches 20.. run function mgs:v5.0.0/player/dps_snapshot

# Decrement special durations (instant_kill, infinite_ammo)
execute if score @s mgs.special.instant_kill matches 1.. run scoreboard players remove @s mgs.special.instant_kill 1
execute if score @s mgs.special.infinite_ammo matches 1.. run scoreboard players remove @s mgs.special.infinite_ammo 1

# Remove temporary tag
tag @s remove mgs.ticking

# Set previous selected weapon (length of string)
execute store result score @s mgs.previous_selected run data get storage mgs:gun SelectedItem.id

# Enable /trigger for this player
scoreboard players enable @s mgs.player.config
execute if score @s mgs.player.config matches 1.. run function mgs:v5.0.0/player/config/process

# Map editor tick (particles + actionbar) for players in editor mode
execute if score @s mgs.mp.map_edit matches 1 run function mgs:v5.0.0/maps/editor/tick

# Multiplayer: detect respawn (death_count incremented by deathCount criterion)
execute if data storage mgs:multiplayer game{state:"active"} if score @s mgs.mp.death_count matches 1.. run function mgs:v5.0.0/multiplayer/on_respawn

