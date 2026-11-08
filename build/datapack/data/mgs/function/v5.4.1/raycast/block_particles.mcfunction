
#> mgs:v5.4.1/raycast/block_particles
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/raycast/on_entry_point with storage mgs:input with
#
# @args		block (string)
#

$particle block{block_state:"$(block)"} ~ ~ ~ 0.1 0.1 0.1 1 10 force @a[distance=..128]

