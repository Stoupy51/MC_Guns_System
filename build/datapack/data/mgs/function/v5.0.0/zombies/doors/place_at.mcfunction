
#> mgs:v5.0.0/zombies/doors/place_at
#
# @within	mgs:v5.0.0/zombies/doors/setup_iter with storage mgs:temp _door
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			block (unknown)
#

# Place door block at position
$setblock $(x) $(y) $(z) $(block)

# Summon interaction entity
$summon minecraft:interaction $(x) $(y) $(z) {width:1.0f,height:1.0f,response:true,Tags:["mgs.door","mgs.gm_entity","bs.entity.interaction","_door_new"]}

