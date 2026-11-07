
#> mgs:v5.4.0/zombies/mystery_box/summon_pos_at
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/mystery_box/setup_pos_iter with storage mgs:temp _mb_pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:2.0f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["mgs.mystery_box_pos","mgs.zombies_entity","mgs.mb_new","bs.entity.interaction"]}

