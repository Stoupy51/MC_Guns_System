
#> mgs:v5.1.0/maps/editor/displays/summon_mystery_box
#
# @executed	positioned ^ ^2 ^0.3
#
# @within	mgs:v5.1.0/maps/editor/displays/mystery_box_pos with storage mgs:temp _ed_mb [ positioned ^ ^2 ^0.3 ]
#
# @args		yaw (unknown)
#

# Same models/scale as zombies/mystery_box/summon_presence_display
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.editor_display"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_base"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.editor_display"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_lid"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}

