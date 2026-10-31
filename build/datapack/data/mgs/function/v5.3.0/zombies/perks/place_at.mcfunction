
#> mgs:v5.3.0/zombies/perks/place_at
#
# @within	mgs:v5.3.0/zombies/perks/setup_iter with storage mgs:temp _pk
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#			perk_id (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:1.2f,height:-2.0f,response:true,Rotation:$(rotation),CustomName:"Perk Machine $(perk_id)",Tags:["mgs.perk_machine","mgs.zombies_entity","bs.entity.interaction","mgs.pk_new"]}

