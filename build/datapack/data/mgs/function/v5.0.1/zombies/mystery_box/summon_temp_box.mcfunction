
#> mgs:v5.0.1/zombies/mystery_box/summon_temp_box
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.1/zombies/mystery_box/fire_sale_summon_box with storage mgs:temp _mb_fs
#
# @args		yaw (unknown)
#

$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_presence","mgs.mb_base","mgs.mb_temp","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_base"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_presence","mgs.mb_lid","mgs.mb_temp","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_lid"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}

