
#> mgs:v5.0.0/multiplayer/gamemodes/hp/summon_marker
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone with storage mgs:temp _hp_pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			label (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.hp_marker","mgs.gm_entity"]}
$summon minecraft:text_display $(x) $(y) $(z) {Tags:["mgs.hp_label","mgs.gm_entity","mgs.hp_$(label)"],billboard:"vertical",text:{"text":"$(label)","color":"dark_purple","bold":true},transformation:{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

