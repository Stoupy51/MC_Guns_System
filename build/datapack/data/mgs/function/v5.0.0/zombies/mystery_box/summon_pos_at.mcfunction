
#> mgs:v5.0.0/zombies/mystery_box/summon_pos_at
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_pos_iter with storage mgs:temp _mbpos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:interaction $(x) $(y) $(z) {width:1.0f,height:1.0f,response:true,Tags:["mgs.mystery_box_pos","mgs.gm_entity","mgs.mb_new","bs.entity.interaction"]}

