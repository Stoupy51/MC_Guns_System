
#> mgs:v5.0.0/zoom/crosshair_spread
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/zoom/main
#

# If sneaking in the air, treat as walking (not jump spread)
execute unless predicate mgs:v5.0.0/is_on_ground if predicate mgs:v5.0.0/is_sneaking at @s anchored eyes run return run particle minecraft:dust{color:[0.02,0.0,0.12],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Jump (in air, not sneaking): widest spread
execute unless predicate mgs:v5.0.0/is_on_ground at @s anchored eyes run return run particle minecraft:dust{color:[0.02,0.0,0.60],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Sprint: very wide spread
execute if predicate mgs:v5.0.0/is_sprinting at @s anchored eyes run return run particle minecraft:dust{color:[0.02,0.0,0.28],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Walk: wider spread
execute unless predicate mgs:v5.0.0/is_sprinting if predicate mgs:v5.0.0/is_moving at @s anchored eyes run return run particle minecraft:dust{color:[0.02,0.0,0.12],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Sneak: tightest spread (rarely visible since sneak = zoom for guns)
execute if predicate mgs:v5.0.0/is_sneaking at @s anchored eyes run return run particle minecraft:dust{color:[0.02,0.0,0.02],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# Base: standing still, default spread
execute at @s anchored eyes run particle minecraft:dust{color:[0.02,0.0,0.05],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

