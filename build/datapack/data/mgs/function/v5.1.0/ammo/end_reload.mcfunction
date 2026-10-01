
#> mgs:v5.1.0/ammo/end_reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# The reload is complete: consume magazines now (single-shell weapons load one bullet per cycle, even with no_magazine).
execute if data storage mgs:config no_magazine unless data storage mgs:gun all.stats.single_reload store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity
execute if data storage mgs:config no_magazine if data storage mgs:gun all.stats.single_reload run function mgs:v5.1.0/ammo/single_reload_add_one
execute unless data storage mgs:config no_magazine run function mgs:v5.1.0/ammo/inventory/find with storage mgs:gun all.stats

execute if data storage mgs:gun all.gun run function mgs:v5.1.0/ammo/modify_lore {slot:"weapon.mainhand"}

tag @s remove mgs.reloading

# Next shell unless full, out of ammo, or firing.
execute if data storage mgs:gun all.stats.single_reload run function mgs:v5.1.0/ammo/single_reload_continue

