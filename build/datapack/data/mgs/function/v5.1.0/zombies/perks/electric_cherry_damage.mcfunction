
#> mgs:v5.1.0/zombies/perks/electric_cherry_damage
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/electric_cherry_shock with storage mgs:temp _ec
#
# @args		radius (unknown)
#			scale (unknown)
#

$execute as @e[tag=mgs.zombie_round,distance=..$(radius)] run function mgs:v5.1.0/zombies/perks/electric_cherry_hit {scale:"$(scale)"}

