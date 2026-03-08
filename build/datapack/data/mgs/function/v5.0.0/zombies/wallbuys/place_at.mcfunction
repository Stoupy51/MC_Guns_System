
#> mgs:v5.0.0/zombies/wallbuys/place_at
#
# @within	mgs:v5.0.0/zombies/wallbuys/setup_iter with storage mgs:temp _wb
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

# Summon interaction entity
$summon minecraft:interaction $(x) $(y) $(z) {width:1.0f,height:1.0f,response:true,Tags:["mgs.wallbuy","mgs.gm_entity","bs.entity.interaction","_wb_new"]}

# Summon item display (floating weapon centered on player view)
$summon minecraft:item_display $(x) $(y) $(z) {billboard:"center",Tags:["mgs.wallbuy_display","mgs.gm_entity","_wb_new_display"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[0.6f,0.6f,0.6f]}}

