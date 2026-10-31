
#> mgs:v5.3.0/zombies/doors/place_at
#
# @within	mgs:v5.3.0/zombies/doors/setup_iter with storage mgs:temp _door
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			block (unknown)
#			facing (unknown)
#			link (unknown)
#

$setblock $(x) $(y) $(z) $(block)

$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^0.75 {width:1.5f,height:1.1f,response:true,Tags:["mgs.door","mgs.door_front","mgs.zombies_entity","bs.entity.interaction","mgs.door_new"],CustomName:"Door link $(link)"}

$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^-0.75 {width:1.5f,height:1.1f,response:true,Tags:["mgs.door","mgs.door_back","mgs.zombies_entity","bs.entity.interaction","mgs.door_new"],CustomName:"Door link $(link) (back)"}

