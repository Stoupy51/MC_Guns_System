
#> stoupgun:v5.0.0/player/right_click
#
# @within	stoupgun:v5.0.0/player/tick
#

# Decrease pending clicks by 1 and stop if cooldown
scoreboard players remove @s stoupgun.pending_clicks 1
execute if score @s stoupgun.cooldown matches 1.. run return fail

# Stop if SelectedItem is not a gun
execute unless data storage stoupgun:gun stats run return fail

# Set cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun stats.cooldown

# Check which type of movement the player is doing
function stoupgun:v5.0.0/raycast/accuracy/get_value

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function stoupgun:v5.0.0/raycast/main

# Simulate weapon kick
function stoupgun:v5.0.0/kicks/main

# Drop casing
function stoupgun:v5.0.0/casing/main

# Handle remaining ammo
function stoupgun:v5.0.0/ammo/main

# Advanced Playsound
function stoupgun:v5.0.0/sound/main

