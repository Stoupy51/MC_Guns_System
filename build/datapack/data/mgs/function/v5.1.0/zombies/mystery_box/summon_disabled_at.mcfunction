
#> mgs:v5.1.0/zombies/mystery_box/summon_disabled_at
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/summon_disabled_display with storage mgs:temp _mb_dis
#			mgs:v5.1.0/zombies/mystery_box/summon_disabled_display with storage mgs:temp _mb_dis [ positioned ~ ~512 ~ ]
#
# @args		yaw (unknown)
#

$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.mb_disabled","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_disabled"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}

