
#> mgs:v5.0.0/ammo/reload
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#			mgs:v5.0.0/player/swap_and_reload
#

# Stop if already reloading, or already has full ammo
execute if entity @s[tag=mgs.reloading] run return fail
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute if score @s mgs.remaining_bullets >= #capacity mgs.data run return fail

# Get the new ammo count
scoreboard players set @s mgs.cooldown 5
execute if data storage mgs:config no_magazine store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute unless data storage mgs:config no_magazine store success score #success mgs.data run function mgs:v5.0.0/ammo/inventory/find with storage mgs:gun all.stats
execute unless data storage mgs:config no_magazine if score #success mgs.data matches 0 run return run playsound mgs:common/empty ambient @s

# Set cooldown to reload duration
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.reload_time

# Force weapon switch animation
function mgs:v5.0.0/switch/force_switch_animation

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Play reload sound (and send sounds for macro)
function mgs:v5.0.0/sound/reload_start with storage mgs:gun all.sounds

# Add reloading tag
tag @s add mgs.reloading

