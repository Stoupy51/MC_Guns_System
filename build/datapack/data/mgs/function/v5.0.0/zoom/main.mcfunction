
#> mgs:v5.0.0/zoom/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# If no gun data, stop here
execute unless data storage mgs:gun all.gun run return run function mgs:v5.0.0/zoom/check_slowness

# If already zoom and not sneaking, unzoom
execute if data storage mgs:gun all.stats.is_zoom unless predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage mgs:gun all.stats.is_zoom if predicate mgs:v5.0.0/is_sneaking run return run function mgs:v5.0.0/zoom/set

## Shader: zoom marker with delay, scope check, and cooldown guard
# Reset zoom timer when not zooming
execute unless score @s mgs.zoom matches 1 run scoreboard players set @s mgs.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s mgs.zoom matches 1 run scoreboard players add @s mgs.zoom_timer 1

# Spawn zoom x3 marker for _3 weapons (scope_level:3) — blocked during weapon switch cooldown
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. if items entity @s weapon.mainhand *[custom_data~{mgs:{scope_level:3}}] at @s anchored eyes run particle minecraft:dust{color:[0.02,0.02,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Spawn zoom x4 marker for _4 weapons (scope_level:4) — blocked during weapon switch cooldown
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. if items entity @s weapon.mainhand *[custom_data~{mgs:{scope_level:4}}] at @s anchored eyes run particle minecraft:dust{color:[0.02,0.08,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Spawn zoom center-only marker (mode 2) for weapons WITHOUT scope — centers flash spark w/o barrel distortion
execute if score @s mgs.zoom matches 1 if score @s mgs.switch_cooldown matches 0 if score @s mgs.zoom_timer matches 5.. unless items entity @s weapon.mainhand *[custom_data~{mgs:{scope_level:3}}] unless items entity @s weapon.mainhand *[custom_data~{mgs:{scope_level:4}}] at @s anchored eyes run particle minecraft:dust{color:[0.02,0.25,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

