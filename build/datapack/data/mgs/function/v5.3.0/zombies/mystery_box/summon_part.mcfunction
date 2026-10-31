
#> mgs:v5.3.0/zombies/mystery_box/summon_part
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s & positioned ~ ~-0.9 ~
#
# @within	mgs:v5.3.0/zombies/mystery_box/summon_presence {tags:["mgs.mb_presence","mgs.mb_base","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],name:"Mystery Box",model:"mgs:mystery_box_base"}
#			mgs:v5.3.0/zombies/mystery_box/summon_presence {tags:["mgs.mb_presence","mgs.mb_lid","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],name:"Mystery Box Lid",model:"mgs:mystery_box_lid"}
#			mgs:v5.3.0/zombies/mystery_box/summon_disabled_display {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],name:"Mystery Box (inactive)",model:"mgs:mystery_box_disabled"} [ positioned ~ ~-0.9 ~ ]
#			mgs:v5.3.0/zombies/mystery_box/summon_disabled_display {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],name:"Mystery Box (inactive)",model:"mgs:mystery_box_disabled"} [ positioned ~ ~511.1 ~ ]
#			mgs:v5.3.0/maps/editor/displays/mystery_box_parts {tags:["mgs.editor_display","mgs.mb_part_new"],name:"Mystery Box",model:"mgs:mystery_box_base"}
#			mgs:v5.3.0/maps/editor/displays/mystery_box_parts {tags:["mgs.editor_display","mgs.mb_part_new"],name:"Mystery Box",model:"mgs:mystery_box_lid"}
#
# @args		tags (list)
#			name (string)
#			model (string)
#

$summon minecraft:item_display ~ ~ ~ {Tags:$(tags),CustomName:"$(name)",item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"$(model)"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
tp @n[tag=mgs.mb_part_new] ~ ~ ~ ~ ~
scoreboard players operation @n[tag=mgs.mb_part_new] mgs.mb.roll = @s mgs.mb.roll
execute as @n[tag=mgs.mb_part_new] run function mgs:v5.3.0/zombies/mystery_box/roll_closed
tag @n[tag=mgs.mb_part_new] remove mgs.mb_part_new

