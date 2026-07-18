
#> mgs:v5.1.0/zombies/display/summon_machine_display
#
# @executed	as @n[tag=mgs.pap_new] & at @s & positioned ^ ^ ^-0.49 & positioned ~ ~-0.4 ~
#
# @within	mgs:v5.1.0/zombies/pap/setup_iter with storage mgs:temp _pap_disp [ as @n[tag=mgs.pap_new] & at @s & positioned ^ ^ ^-0.49 & positioned ~ ~-0.4 ~ ]
#			mgs:v5.1.0/zombies/perks/setup_iter with storage mgs:temp _pk_disp [ as @n[tag=mgs.pk_new] & at @s & align xyz & positioned ~.5 ~-.37 ~.5 & positioned ^ ^ ^-0.49 ]
#			mgs:v5.1.0/maps/editor/displays/perk_machine with storage mgs:temp _pk_disp [ align xyz & positioned ~.5 ~-.37 ~.5 & positioned ^ ^ ^-0.49 ]
#			mgs:v5.1.0/maps/editor/displays/pap_machine with storage mgs:temp _pap_disp [ positioned ^ ^ ^-0.49 & positioned ~ ~-0.4 ~ ]
#
# @args		yaw (unknown)
#			tag (unknown)
#			item_id (unknown)
#			item_model (unknown)
#

$summon minecraft:item_display ~ ~1.0 ~ {Rotation:[$(yaw)f,0f],Tags:["$(tag)","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"$(item_id)",count:1,components:{"minecraft:item_model":"$(item_model)"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.25f,1.25f,1.25f]}}

