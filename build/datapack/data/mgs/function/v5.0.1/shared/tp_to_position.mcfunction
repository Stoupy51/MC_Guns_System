
#> mgs:v5.0.1/shared/tp_to_position
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.0.1/zombies/start with storage mgs:temp _tp [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.0.1/missions/start with storage mgs:temp _tp [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.0.1/maps/editor/enter with storage mgs:temp _tp
#			mgs:v5.0.1/maps/editor/invite_all with storage mgs:temp _tp [ as @a[scores={mgs.mp.map_edit=1}] ]
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$tp @s $(x) $(y) $(z)

