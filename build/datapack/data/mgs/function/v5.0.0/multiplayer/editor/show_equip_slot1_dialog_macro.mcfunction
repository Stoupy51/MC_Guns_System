
#> mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_equipment_slot_1",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",{"translate": "mgs.points_remaining","color":"white"},{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate: "mgs.choose_grenade_for_slot_1_hotbar_8_1_pt_if_not_none",color:"gray"}}],actions:[{label:{translate: "mgs.none",color:"green"},tooltip:{translate: "mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 460"}},{label:{translate: "mgs.frag_grenade",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 461"}},{label:{translate: "mgs.semtex",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 462"}},{label:{translate: "mgs.flash",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 463"}},{label:{translate: "mgs.smoke",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 464"}}],columns:3,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 360"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

