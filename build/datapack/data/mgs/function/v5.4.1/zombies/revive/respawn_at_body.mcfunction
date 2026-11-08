
#> mgs:v5.4.1/zombies/revive/respawn_at_body
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/respawn_near_player with storage mgs:temp _body
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute in $(dimension) positioned $(x) $(y) $(z) run function mgs:v5.4.1/zombies/revive/respawn_from_body

