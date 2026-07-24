
#> mgs:v5.1.0/multiplayer/editor/show_static_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/show_primary_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_secondary_pistol_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_secondary_overkill_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_full with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_no4 with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_1only with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_primary_camo_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_equip1_camo_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_equip2_camo_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot1_dialog with storage mgs:temp _dlg
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog with storage mgs:temp _dlg
#
# @args		title (unknown)
#			pts (unknown)
#			hint (unknown)
#			columns (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:$(title),body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:$(hint)}],actions:[],columns:$(columns),after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}}

