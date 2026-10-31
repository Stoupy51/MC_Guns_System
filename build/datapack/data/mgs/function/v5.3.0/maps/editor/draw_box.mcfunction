
#> mgs:v5.3.0/maps/editor/draw_box
#
# @executed	as @a[scores={mgs.mp.map_edit=1}] & at @s & as @e[type=minecraft:marker,tag=mgs.ed_box,distance=..32]
#
# @within	mgs:v5.3.0/maps/editor/particles with entity @s data._ed.box [ as @a[scores={mgs.mp.map_edit=1}] & at @s & as @e[type=minecraft:marker,tag=mgs.ed_box,distance=..32] ]
#
# @args		x2 (unknown)
#			y1 (unknown)
#			z1 (unknown)
#			x1 (unknown)
#			z2 (unknown)
#			y2 (unknown)
#

$particle trail{target:[$(x2),$(y1),$(z1)],color:5635925,duration:20} $(x1) $(y1) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y1),$(z2)],color:5635925,duration:20} $(x1) $(y1) $(z2) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y2),$(z1)],color:5635925,duration:20} $(x1) $(y2) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y2),$(z2)],color:5635925,duration:20} $(x1) $(y2) $(z2) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x1),$(y2),$(z1)],color:5635925,duration:20} $(x1) $(y1) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x1),$(y2),$(z2)],color:5635925,duration:20} $(x1) $(y1) $(z2) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y2),$(z1)],color:5635925,duration:20} $(x2) $(y1) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y2),$(z2)],color:5635925,duration:20} $(x2) $(y1) $(z2) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x1),$(y1),$(z2)],color:5635925,duration:20} $(x1) $(y1) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x1),$(y2),$(z2)],color:5635925,duration:20} $(x1) $(y2) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y1),$(z2)],color:5635925,duration:20} $(x2) $(y1) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]
$particle trail{target:[$(x2),$(y2),$(z2)],color:5635925,duration:20} $(x2) $(y2) $(z1) 0 0 0 0 1 force @a[scores={mgs.mp.map_edit=1},distance=..48]

