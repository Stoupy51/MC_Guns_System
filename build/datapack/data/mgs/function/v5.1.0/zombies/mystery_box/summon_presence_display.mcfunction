
#> mgs:v5.1.0/zombies/mystery_box/summon_presence_display
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/sync_presence_display with storage mgs:temp _mb_chest [ as @n[tag=mgs.mystery_box_active] & at @s ]
#
# @args		yaw (unknown)
#

# Two-piece presence box: base + lid (both tagged mb_presence so they move/despawn together).
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_presence","mgs.mb_base","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_base"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_presence","mgs.mb_lid","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_lid"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}

