
#> stoupgun:v5.0.0/player/tick
#
# @within	stoupgun:v5.0.0/tick
#

# Add temporary tag
tag @s add stoupgun.ticking

# Copy gun data
data remove storage stoupgun:gun stats
data modify storage stoupgun:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".stoupgun.stats

# Check if we need to zoom weapon or stop
function stoupgun:v5.0.0/zoom/main

# Check if switching weapon
function stoupgun:v5.0.0/switch/main

# If pending clicks, run function
execute if score @s stoupgun.cooldown matches 1.. run scoreboard players remove @s stoupgun.cooldown 1
execute if score @s stoupgun.pending_clicks matches -100.. run function stoupgun:v5.0.0/player/right_click

# TODO: Title action bar that shows bullet icons (grayed = no bullet) instead of count/max_count

# Remove temporary tag
tag @s remove stoupgun.ticking

