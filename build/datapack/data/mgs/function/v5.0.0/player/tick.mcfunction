
#> mgs:v5.0.0/player/tick
#
# @within	mgs:v5.0.0/tick
#

# Add temporary tag
tag @s add mgs.ticking

# Compute acoustics (#TODO: Only if player moved enough, and every second not tick)
function mgs:v5.0.0/sound/compute_acoustics

# Copy gun data
data remove storage mgs:gun all
data modify storage mgs:gun SelectedItem set value {id:""}
data modify storage mgs:gun SelectedItem set from entity @s SelectedItem
data modify storage mgs:gun all set from storage mgs:gun SelectedItem.components."minecraft:custom_data".mgs

# Check if we need to zoom weapon or stop
function mgs:v5.0.0/zoom/main

# Check if switching weapon
function mgs:v5.0.0/switch/main

# Decrease cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# Check if we need to play reload end sound
execute if score @s mgs.cooldown matches 1.. if data storage mgs:gun all.stats run function mgs:v5.0.0/sound/check_reload_end
execute if score @s mgs.cooldown matches 0 if entity @s[tag=mgs.reloading] run function mgs:v5.0.0/ammo/end_reload

# If pending clicks, run right click function
execute if score @s mgs.pending_clicks matches -100.. run function mgs:v5.0.0/player/right_click

# TODO: Title action bar that shows bullet icons (grayed = no bullet) instead of count/max_count

# Remove temporary tag
tag @s remove mgs.ticking

# Set previous selected weapon (length of string)
execute store result score @s mgs.previous_selected run data get storage mgs:gun SelectedItem.id

