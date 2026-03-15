
#> mgs:v5.0.0/zombies/doors/place_at
#
# @within	mgs:v5.0.0/zombies/doors/setup_iter with storage mgs:temp _door
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			block (unknown)
#			facing (unknown)
#

# Place door block at position
$setblock $(x) $(y) $(z) $(block)

# Summon front-side interaction entity.
$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^0.5 {width:1.5f,height:1.1f,response:true,Tags:["mgs.door","mgs.door_front","mgs.gm_entity","bs.entity.interaction","mgs.door_new"]}

# Summon back-side interaction entity.
$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^-0.5 {width:1.5f,height:1.1f,response:true,Tags:["mgs.door","mgs.door_back","mgs.gm_entity","bs.entity.interaction","mgs.door_new"]}

