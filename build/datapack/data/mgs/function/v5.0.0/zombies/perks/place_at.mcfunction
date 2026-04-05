
#> mgs:v5.0.0/zombies/perks/place_at
#
# @within	mgs:v5.0.0/zombies/perks/setup_iter with storage mgs:temp _pk
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:1.0f,height:2.0f,response:true,Rotation:$(rotation),Tags:["mgs.perk_machine","mgs.gm_entity","bs.entity.interaction","mgs.pk_new"]}

