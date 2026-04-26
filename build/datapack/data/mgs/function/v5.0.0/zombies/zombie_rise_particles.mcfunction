
#> mgs:v5.0.0/zombies/zombie_rise_particles
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/zombie_rise_tick with storage mgs:temp _rise_particle
#
# @args		block (unknown)
#

$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~1 ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]

