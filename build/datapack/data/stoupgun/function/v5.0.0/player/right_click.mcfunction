
#> stoupgun:v5.0.0/player/right_click
#
# @within	stoupgun:v5.0.0/player/tick
#

# Decrease pending clicks by 1 and stop if cooldown
scoreboard players remove @s stoupgun.pending_clicks 1
execute if score @s stoupgun.cooldown matches 1.. run return fail

# Copy gun data, stop if SelectedItem is not a gun
data remove storage stoupgun:gun stats
data modify storage stoupgun:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".stoupgun.stats
execute unless data storage stoupgun:gun stats run return fail

# Set cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun stats.cooldown

# Shoot with raycast using https://docs.mcbookshelf.dev/en/latest/modules/raycast.html
function stoupgun:v5.0.0/raycast/main

# Simulate weapon kick
function stoupgun:v5.0.0/kicks/main

# Drop casing
function stoupgun:v5.0.0/casing/main

# Handle remaining ammo
function stoupgun:v5.0.0/ammo/main

# Advanced Playsound
function stoupgun:v5.0.0/sound/main

