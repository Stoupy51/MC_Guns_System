
#> mgs:v5.0.0/ammo/reload
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#			mgs:v5.0.0/player/swap_and_reload
#

# Get the new ammo count
scoreboard players set @s mgs.cooldown 5
execute if data storage mgs:config no_magazine store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute unless data storage mgs:config no_magazine run function mgs:v5.0.0/ammo/inventory/find with storage mgs:gun all.stats
execute unless data storage mgs:config no_magazine unless score #found_ammo mgs.data matches 1.. run return run playsound mgs:common/empty ambient @s

# Set cooldown to reload duration
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.reload_time

# Force weapon switch animation
function mgs:v5.0.0/switch/force_switch_animation

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Play reload sound (and send stats for macro)
function mgs:v5.0.0/sound/reload_start with storage mgs:gun all.stats

# Add reloading tag
tag @s add mgs.reloading

