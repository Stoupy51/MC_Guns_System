
#> mgs:v5.0.0/raycast/block_particles
#
# @within	mgs:v5.0.0/raycast/on_hit_point with storage mgs:input with
#

$particle block{block_state:"$(block)"} $(x) $(y) $(z) 0.1 0.1 0.1 1 10 force @a[distance=..128]

