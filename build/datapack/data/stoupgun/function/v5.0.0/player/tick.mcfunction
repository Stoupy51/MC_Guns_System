
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
execute if data storage stoupgun:gun stats run function stoupgun:v5.0.0/zoom/main

# If pending clicks, run function
execute if score @s stoupgun.cooldown matches 1.. run scoreboard players remove @s stoupgun.cooldown 1
execute if score @s stoupgun.pending_clicks matches 1.. run function stoupgun:v5.0.0/player/right_click

# Remove temporary tag
tag @s remove stoupgun.ticking

