
#> stoupgun:v5.0.0/player/right_click
#
# @within	stoupgun:v5.0.0/player/tick
#

# Decrease pending clicks by 1
scoreboard players remove @s stoupgun.pending_clicks 1

# If player stopped right clicking for 1 second, we update the item lore
execute if score @s stoupgun.pending_clicks matches -20 run function stoupgun:v5.0.0/ammo/modify_lore {slot:"$(slot)"}

# Stop here is weapon cooldown OR pending clicks if negative
execute if score @s stoupgun.cooldown matches 1.. run return fail
execute if score @s stoupgun.pending_clicks matches ..-1 run return fail

# Stop if SelectedItem is not a gun or if not enough ammo
execute unless data storage stoupgun:gun all.stats run return fail
execute if score @s stoupgun.remaining_bullets matches ..0 run return run function stoupgun:v5.0.0/ammo/reload

# Set cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun all.stats.cooldown

# Check which type of movement the player is doing
function stoupgun:v5.0.0/raycast/accuracy/get_value

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function stoupgun:v5.0.0/raycast/main

# Simulate weapon kick
function stoupgun:v5.0.0/kicks/main

# Drop casing
function stoupgun:v5.0.0/casing/main

# Decrease bullet count
function stoupgun:v5.0.0/ammo/decrease

# Advanced Playsound
function stoupgun:v5.0.0/sound/main

