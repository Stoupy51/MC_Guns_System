
#> stoupgun:v5.0.0/ammo/reload
#
# @within	stoupgun:v5.0.0/player/right_click
#

# Set cooldown to reload duration
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun all.stats.reload_time

# Get the new ammo count
# TODO: Find ammo in inventory and don't take it out for your ass
execute store result score @s stoupgun.remaining_bullets run data get storage stoupgun:gun all.stats.capacity

# Play reload sound (and send stats for macro)
function stoupgun:v5.0.0/sound/reload_start with storage stoupgun:gun all.stats

# Add reloading tag
tag @s add stoupgun.reloading

