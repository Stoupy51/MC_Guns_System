
#> mgs:v5.4.0/lobby/teleport
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/lobby/return with storage mgs:config lobby
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#			yaw (unknown)
#			pitch (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)

