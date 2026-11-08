
#> mgs:v5.4.1/zombies/pap/place_at
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/pap/setup_iter with storage mgs:temp _pap_place
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:1.69f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["mgs.pap_machine","mgs.zombies_entity","bs.entity.interaction","mgs.pap_new"]}

