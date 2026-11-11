
#> mgs:v5.4.2/lobby/teleport
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/lobby/return with storage mgs:config lobby
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#			yaw (unknown)
#			pitch (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)

