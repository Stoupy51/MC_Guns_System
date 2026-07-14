
#> mgs:v5.1.0/multiplayer/enforce_bounds
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/game_tick [ at @s ]
#

# Coordinate bounds (only when the map defines a boundary box). May eliminate @s -> spectator.
execute if score #mp_has_boundary mgs.data matches 1 run function mgs:v5.1.0/multiplayer/check_bounds

# OOB markers. Skip if the coordinate check just eliminated @s this tick (now a spectator) — the
# original two-pass form excluded such players via its gamemode=!spectator selector, so doing the
# OOB kill here too would double-count the death.
execute if entity @s[gamemode=!spectator] if entity @e[tag=mgs.oob_point,distance=..5] run function mgs:v5.1.0/multiplayer/bounds_kill

