
#> mgs:v5.1.0/zombies/barricades/freeze_zombies
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

$execute as @e[tag=mgs.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add mgs:freeze -1024 add_multiplied_total
$tag @e[tag=mgs.zombie_round,distance=..$(radius)] add mgs.barricade_frozen

# Escort taxis are not zombie_round, so the freeze misses them and the glued zombie would walk through.
# Ending the escort hands the zombie back to normal AI, and the freeze catches it next tick.
$execute as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..$(radius)] at @s run function mgs:v5.1.0/zombies/escort/end_at_trader

