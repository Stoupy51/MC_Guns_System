
#> mgs:v5.2.0/lobby/teleport
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.2.0/lobby/return with storage mgs:config lobby
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#			yaw (unknown)
#			pitch (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)

