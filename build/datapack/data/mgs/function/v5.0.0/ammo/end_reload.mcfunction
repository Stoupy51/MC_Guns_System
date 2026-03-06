
#> mgs:v5.0.0/ammo/end_reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Actually consume magazines and update ammo now that reload is complete
execute if data storage mgs:config no_magazine store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute unless data storage mgs:config no_magazine run function mgs:v5.0.0/ammo/inventory/find with storage mgs:gun all.stats

# Update weapon lore (if still holding weapon)
execute if data storage mgs:gun all.gun run function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Remove reloading tag
tag @s remove mgs.reloading

