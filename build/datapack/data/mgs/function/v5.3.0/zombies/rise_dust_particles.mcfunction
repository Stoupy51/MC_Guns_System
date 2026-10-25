
#> mgs:v5.3.0/zombies/rise_dust_particles
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/rise_dust_tick with entity @s data
#
# @args		block (unknown)
#

$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~ ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]

