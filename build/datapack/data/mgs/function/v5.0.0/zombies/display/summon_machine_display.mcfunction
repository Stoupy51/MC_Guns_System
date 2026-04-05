
#> mgs:v5.0.0/zombies/display/summon_machine_display
#
# @executed	as @n[tag=mgs.pap_new] & at @s
#
# @within	mgs:v5.0.0/zombies/pap/setup_iter with storage mgs:temp _pap_disp [ as @n[tag=mgs.pap_new] & at @s ]
#			mgs:v5.0.0/zombies/pap/anim_restore_display_lookup with storage mgs:temp _pap_restore_disp
#			mgs:v5.0.0/zombies/perks/setup_iter with storage mgs:temp _pk_disp [ as @n[tag=mgs.pk_new] & at @s ]
#
# @args		tag (unknown)
#			item_id (unknown)
#			item_model (unknown)
#

$summon minecraft:item_display ~ ~1.0 ~ {Tags:["$(tag)","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"$(item_id)",count:1,components:{"minecraft:item_model":"$(item_model)"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}}

