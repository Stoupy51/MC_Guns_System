
#> mgs:v5.0.0/raycast/air_particles
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/on_hit_point with storage mgs:input with
#
# @args		block (string)
#			x (int)
#			y (int)
#			z (int)
#

$particle $(block) $(x) $(y) $(z) 0 0 0 0 1 force @a[distance=..128]

