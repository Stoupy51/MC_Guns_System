
#> mgs:v5.0.0/player/tick
#
# @within	mgs:v5.0.0/tick
#

# Add temporary tag
tag @s add mgs.ticking

# Copy gun data
data remove storage mgs:gun all
data modify storage mgs:gun all set from entity @s SelectedItem.components."minecraft:custom_data".mgs

# Check if we need to zoom weapon or stop
function mgs:v5.0.0/zoom/main

# Check if switching weapon
function mgs:v5.0.0/switch/main

# Decrease cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# Check if we need to play reload end sound
execute if score @s mgs.cooldown matches 1.. if data storage mgs:gun all.stats run function mgs:v5.0.0/sound/check_reload_end

# If pending clicks, run right click function
execute if score @s mgs.pending_clicks matches -100.. run function mgs:v5.0.0/player/right_click

# TODO: Title action bar that shows bullet icons (grayed = no bullet) instead of count/max_count

# Remove temporary tag
tag @s remove mgs.ticking

