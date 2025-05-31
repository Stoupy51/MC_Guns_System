
#> mgs:v5.0.0/ammo/reload
#
# @within	mgs:v5.0.0/player/right_click
#

# Set cooldown to reload duration
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.reload_time

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Get the new ammo count
# TODO: Find ammo in inventory and don't take it out for your ass
execute store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity

# Play reload sound (and send stats for macro)
function mgs:v5.0.0/sound/reload_start with storage mgs:gun all.stats

# Add reloading tag
tag @s add mgs.reloading

