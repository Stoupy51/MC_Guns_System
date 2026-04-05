
#> mgs:v5.0.0/zombies/mystery_box/summon_presence_display
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.0.0/zombies/mystery_box/sync_presence_display with storage mgs:temp _mb_chest [ as @n[tag=mgs.mystery_box_active] & at @s ]
#
# @args		yaw (unknown)
#

$execute positioned ~ ~0.7 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_presence","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}}

