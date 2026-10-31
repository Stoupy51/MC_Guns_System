
#> mgs:v5.3.0/zombies/spawns/test_box
#
# @executed	as @e[type=minecraft:marker,tag=...]
#
# @within	mgs:v5.3.0/zombies/spawns/check_box with entity @s data.abox
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			dx (unknown)
#			dy (unknown)
#			dz (unknown)
#

$execute if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run tag @s add mgs.spawn_abox_ok

