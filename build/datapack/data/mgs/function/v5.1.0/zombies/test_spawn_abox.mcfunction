
#> mgs:v5.1.0/zombies/test_spawn_abox
#
# @executed	as @e[tag=mgs.zb_near]
#
# @within	mgs:v5.1.0/zombies/filter_spawn_abox with storage mgs:temp _abox_chk
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			dx (unknown)
#			dy (unknown)
#			dz (unknown)
#

$execute if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,x=$(x),y=$(y),z=$(z),dx=$(dx),dy=$(dy),dz=$(dz)] run scoreboard players set #abox_ok mgs.data 1

