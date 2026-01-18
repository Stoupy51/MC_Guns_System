
#> mgs:v5.0.0/ammo/reload
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Set cooldown to reload duration
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.reload_time

# Force weapon switch animation
function mgs:v5.0.0/switch/force_switch_animation

# Get the new ammo count
execute if data storage mgs:config no_magazine store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute unless data storage mgs:config no_magazine unless function mgs:v5.0.0/ammo/inventory/find run return fail

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Play reload sound (and send stats for macro)
function mgs:v5.0.0/sound/reload_start with storage mgs:gun all.stats

# Add reloading tag
tag @s add mgs.reloading

