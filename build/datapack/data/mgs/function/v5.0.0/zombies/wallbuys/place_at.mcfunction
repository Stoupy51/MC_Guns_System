
#> mgs:v5.0.0/zombies/wallbuys/place_at
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup_iter with storage mgs:temp _wb
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			rotation (unknown)
#

# Summon interaction entity slightly in front of the wall, centered on display height.
$summon minecraft:interaction $(x) $(y) $(z) {width:0.9f,height:1.0f,response:true,Rotation:$(rotation),Tags:["mgs.wallbuy","mgs.gm_entity","bs.entity.interaction","mgs.wb_new"]}

# Summon item display offset toward the wall face.
$summon minecraft:item_display $(x) $(y) $(z) {billboard:"fixed",item_display:"fixed",Rotation:$(rotation),Tags:["mgs.wallbuy_display","mgs.gm_entity","mgs.wb_new_display"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}

