
#> mgs:v5.4.1/ammo/single_reload_continue
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/ammo/end_reload
#

# Lets the player fire mid-reload.
execute if score @s mgs.pending_clicks matches 0.. run return fail

execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute if score @s mgs.remaining_bullets >= #capacity mgs.data run return fail

# No matching ammo left: stop silently.
execute unless data storage mgs:config no_magazine store success score #success mgs.data run function mgs:v5.4.1/ammo/inventory/has_ammo with storage mgs:gun all.stats
execute unless data storage mgs:config no_magazine if score #success mgs.data matches 0 run return fail

# Plays the reload sound and sets a fresh per-shell cooldown.
function mgs:v5.4.1/ammo/reload

