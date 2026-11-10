
#> mgs:v5.4.1/zombies/perks/place_at
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/setup_iter with storage mgs:temp _pk
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:1.2f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["mgs.perk_machine","mgs.zombies_entity","mgs.pk_new"]}

