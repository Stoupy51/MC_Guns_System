
#> mgs:v5.1.0/zoom/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# If no gun data, stop here
execute unless data storage mgs:gun all.gun run return run function mgs:v5.1.0/zoom/check_slowness

# Grenades cannot zoom/aim, but still get the movement crosshair
execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.1.0/zoom/crosshair_spread

# Get is sneaking state (don't apply zoom if reloading)
scoreboard players set #is_sneaking mgs.data 0
execute if predicate mgs:v5.1.0/is_sneaking unless entity @s[tag=mgs.reloading] run scoreboard players set #is_sneaking mgs.data 1

# If already zoom and not sneaking, unzoom
execute if data storage mgs:gun all.stats.is_zoom if score #is_sneaking mgs.data matches 0 run return run function mgs:v5.1.0/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage mgs:gun all.stats.is_zoom if score #is_sneaking mgs.data matches 1 run return run function mgs:v5.1.0/zoom/set

## Shader ids: the scope overlay while aiming, the spread crosshair while not
# Reset zoom timer when not zooming
execute unless score @s mgs.zoom matches 1 run scoreboard players set @s mgs.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s mgs.zoom matches 1 run scoreboard players add @s mgs.zoom_timer 1

# The crosshair is hidden behind the scope, so the two are mutually exclusive
execute if score @s mgs.zoom matches 1 run return run function mgs:v5.1.0/zoom/crosshair_clear
function mgs:v5.1.0/zoom/crosshair_spread

