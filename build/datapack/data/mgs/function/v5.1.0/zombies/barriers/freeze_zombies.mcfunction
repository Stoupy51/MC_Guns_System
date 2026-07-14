
#> mgs:v5.1.0/zombies/barriers/freeze_zombies
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barriers/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

$execute as @e[tag=mgs.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add mgs:freeze -1024 add_multiplied_total
$tag @e[tag=mgs.zombie_round,distance=..$(radius)] add mgs.barrier_frozen

# Escort taxis (invisible wandering traders) ignore the freeze — they aren't zombie_round and the
# glued zombie is force-tp'd onto them each tick, so an escorted zombie would walk straight through
# a barrier. End the escort on contact instead: the zombie drops to normal AI and the freeze above
# catches it next tick, so it respects the barrier (and can remove it) like any other zombie.
$execute as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..$(radius)] at @s run function mgs:v5.1.0/zombies/escort/end_at_trader

