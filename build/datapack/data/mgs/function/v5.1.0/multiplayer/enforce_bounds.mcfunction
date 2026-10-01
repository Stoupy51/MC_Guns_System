
#> mgs:v5.1.0/multiplayer/enforce_bounds
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/game_tick [ at @s ]
#

# Only when the map defines a boundary box; may turn @s into a spectator.
execute unless score @s mgs.mp.bphase matches 0..3 run function mgs:v5.1.0/multiplayer/assign_bphase
execute if score #mp_has_boundary mgs.data matches 1 if score @s mgs.mp.bphase = #bounds_phase mgs.data run function mgs:v5.1.0/multiplayer/check_bounds

# Skipped if the coordinate check just eliminated @s, or the death would count twice.
execute if entity @s[gamemode=!spectator] if entity @e[tag=mgs.oob_point,distance=..5] run function mgs:v5.1.0/multiplayer/bounds_kill

