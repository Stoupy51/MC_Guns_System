
#> mgs:v5.0.1/ammo/single_reload_continue
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/ammo/end_reload
#

# Stop if the player is actively trying to shoot (lets them fire mid-reload)
execute if score @s mgs.pending_clicks matches 0.. run return fail

# Stop if the magazine is already full
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute if score @s mgs.remaining_bullets >= #capacity mgs.data run return fail

# Stop silently if no matching ammo remains in the inventory
execute unless data storage mgs:config no_magazine store success score #success mgs.data run function mgs:v5.0.1/ammo/inventory/has_ammo with storage mgs:gun all.stats
execute unless data storage mgs:config no_magazine if score #success mgs.data matches 0 run return fail

# Load the next shell (plays the reload sound and sets a fresh per-shell cooldown)
function mgs:v5.0.1/ammo/reload

