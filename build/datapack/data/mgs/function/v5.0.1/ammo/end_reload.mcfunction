
#> mgs:v5.0.1/ammo/end_reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/tick
#

# Actually consume magazines and update ammo now that reload is complete
# (single-shell weapons only load one bullet per cycle, even in no_magazine mode)
execute if data storage mgs:config no_magazine unless data storage mgs:gun all.stats.single_reload store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute if data storage mgs:config no_magazine if data storage mgs:gun all.stats.single_reload run function mgs:v5.0.1/ammo/single_reload_add_one
execute unless data storage mgs:config no_magazine run function mgs:v5.0.1/ammo/inventory/find with storage mgs:gun all.stats

# Update weapon lore (if still holding weapon)
execute if data storage mgs:gun all.gun run function mgs:v5.0.1/ammo/modify_lore {slot:"weapon.mainhand"}

# Remove reloading tag
tag @s remove mgs.reloading

# Single-shell reload: chain into the next shell unless full, out of ammo, or the player is firing
execute if data storage mgs:gun all.stats.single_reload run function mgs:v5.0.1/ammo/single_reload_continue

