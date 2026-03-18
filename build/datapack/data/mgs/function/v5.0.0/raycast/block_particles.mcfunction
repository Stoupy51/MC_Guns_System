
#> mgs:v5.0.0/raycast/block_particles
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/on_entry_point with storage mgs:input with
#
# @args		block (string)
#

$particle block{block_state:"$(block)"} ~ ~ ~ 0.1 0.1 0.1 1 10 force @a[distance=..128]

