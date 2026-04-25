
#> mgs:v5.0.0/zombies/barriers/freeze_zombies
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

$execute as @e[tag=mgs.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add mgs:freeze -1024 add_multiplied_total
$tag @e[tag=mgs.zombie_round,distance=..$(radius)] add mgs.barrier_frozen

