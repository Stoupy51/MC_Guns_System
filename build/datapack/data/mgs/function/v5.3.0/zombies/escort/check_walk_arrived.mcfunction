
#> mgs:v5.3.0/zombies/escort/check_walk_arrived
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/escort/walk_ride with entity @s data.walk_to
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute positioned $(x) $(y) $(z) if entity @s[distance=..4] run scoreboard players set #zb_esc_arrived mgs.data 1

