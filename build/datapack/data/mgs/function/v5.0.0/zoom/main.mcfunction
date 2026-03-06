
#> mgs:v5.0.0/zoom/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# If no gun data, stop here
execute unless data storage mgs:gun all.gun run return run function mgs:v5.0.0/zoom/check_slowness

# Grenades cannot zoom/aim
execute if data storage mgs:gun all.stats.grenade_type run return 0

# If already zoom and not sneaking, unzoom
execute if data storage mgs:gun all.stats.is_zoom unless predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage mgs:gun all.stats.is_zoom if predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/set

## Shader: zoom marker with delay, scope check, and cooldown guard
# Reset zoom timer when not zooming
execute unless score @s mgs.zoom matches 1 run scoreboard players set @s mgs.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s mgs.zoom matches 1 run scoreboard players add @s mgs.zoom_timer 1

# FOV marker: spawn IMMEDIATELY on zoom (no delay) for smooth FOV reduction
# Uses color with B=0.15 (non-zero B + non-zero G) to distinguish from zoom/flash/spread markers
# B=0.15 → B'∈[18-38] after randomization, safely above dim grayscale particles
scoreboard players set #scope_level mgs.data 0
execute store result score #scope_level mgs.data run data get storage mgs:gun all.scope_level
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score #scope_level mgs.data matches 3 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.02,0.15],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score #scope_level mgs.data matches 4 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.08,0.15],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 unless score #scope_level mgs.data matches 3 unless score #scope_level mgs.data matches 4 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.25,0.15],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s

# Scope zoom marker: spawn AFTER delay for barrel distortion effect
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. if score #scope_level mgs.data matches 3 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.02,0.0],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. if score #scope_level mgs.data matches 4 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.08,0.0],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. unless score #scope_level mgs.data matches 3 unless score #scope_level mgs.data matches 4 at @s anchored eyes run particle minecraft:dust{color:[0.02,0.25,0.0],scale:0.01} ^ ^ ^0.1 0 0 0 0 1 force @s

# Crosshair spread marker: spawn when NOT zooming to indicate accuracy via crosshair gap
execute unless score @s mgs.zoom matches 1 run function mgs:v5.0.0/zoom/crosshair_spread

