
#> mgs:v5.0.0/player/tick
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/tick [ as @a[sort=random] & at @s ]
#

# Add temporary tag
tag @s add mgs.ticking

# Compute acoustics (#TODO: Only if player moved enough, and every second not tick)
function mgs:v5.0.0/sound/compute_acoustics

# Reload when moving weapon to offhand
execute if items entity @s weapon.offhand * run function mgs:v5.0.0/player/reload_check

# Copy gun data
function mgs:v5.0.0/utils/copy_gun_data

# Check if we need to zoom weapon or stop
function mgs:v5.0.0/zoom/main

# Check if switching weapon
function mgs:v5.0.0/switch/main

# Decrease cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# Check if we need to play reload end sound
execute if score @s mgs.cooldown matches 1.. if data storage mgs:gun all.gun run function mgs:v5.0.0/sound/check_reload_end
execute if score @s mgs.cooldown matches 0 if entity @s[tag=mgs.reloading] run function mgs:v5.0.0/ammo/end_reload

# If pending clicks, run right click function
execute if score @s mgs.pending_clicks matches -100.. run function mgs:v5.0.0/player/right_click

# Show ammo action bar
execute if data storage mgs:gun all.gun run function mgs:v5.0.0/ammo/show_action_bar

# Remove temporary tag
tag @s remove mgs.ticking

# Set previous selected weapon (length of string)
execute store result score @s mgs.previous_selected run data get storage mgs:gun SelectedItem.id

