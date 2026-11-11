
#> mgs:v5.4.2/zombies/mystery_box/summon_part
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/summon_presence {tags:["mgs.mb_presence","mgs.mb_base","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],model:"mgs:mystery_box_base"}
#			mgs:v5.4.2/zombies/mystery_box/summon_presence {tags:["mgs.mb_presence","mgs.mb_lid","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],model:"mgs:mystery_box_lid"}
#			mgs:v5.4.2/zombies/mystery_box/summon_disabled_display {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],model:"mgs:mystery_box_disabled"} [ positioned ~ ~-0.9 ~ ]
#			mgs:v5.4.2/zombies/mystery_box/summon_disabled_display {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],model:"mgs:mystery_box_disabled"} [ positioned ~ ~511.1 ~ ]
#			mgs:v5.4.2/maps/editor/displays/mystery_box_parts {tags:["mgs.ed_disp_new","mgs.mb_part_new"],model:"mgs:mystery_box_base"}
#			mgs:v5.4.2/maps/editor/displays/mystery_box_parts {tags:["mgs.ed_disp_new","mgs.mb_part_new"],model:"mgs:mystery_box_lid"}
#
# @args		tags (list)
#			model (string)
#

$summon minecraft:item_display ~ ~ ~ {Tags:$(tags),item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"$(model)"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
tp @n[tag=mgs.mb_part_new] ~ ~ ~ ~ ~
scoreboard players operation @n[tag=mgs.mb_part_new] mgs.mb.roll = @s mgs.mb.roll
execute as @n[tag=mgs.mb_part_new] run function mgs:v5.4.2/zombies/mystery_box/roll_closed
tag @n[tag=mgs.mb_part_new] remove mgs.mb_part_new

