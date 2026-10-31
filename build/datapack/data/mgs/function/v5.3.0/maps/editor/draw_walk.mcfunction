
#> mgs:v5.3.0/maps/editor/draw_walk
#
# @executed	as @a[scores={mgs.mp.map_edit=1}] & at @s & as @e[type=minecraft:marker,tag=mgs.ed_walk,distance=..32]
#
# @within	mgs:v5.3.0/maps/editor/particles with entity @s data._ed.walk [ as @a[scores={mgs.mp.map_edit=1}] & at @s & as @e[type=minecraft:marker,tag=mgs.ed_walk,distance=..32] ]
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			from_x (unknown)
#			from_y (unknown)
#			from_z (unknown)
#

$particle trail{target:[$(x),$(y),$(z)],color:16755200,duration:20} $(from_x) $(from_y) $(from_z) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle dust{color:[1.0,0.67,0.0],scale:1.5} $(x) $(y) $(z) 0.15 0.15 0.15 0 3 force @a[scores={mgs.mp.map_edit=1},distance=..48]

