
#> mgs:v5.0.0/multiplayer/editor/scope/primary_no4_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/scope/primary_no4 with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_scope",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",{"translate": "mgs.points_remaining","color":"white"},{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_optic_1_pt_for_any_scope_iron_sights_free",color:"gray"}}],actions:[{label:{translate: "mgs.iron_sights",color:"green"},tooltip:{translate: "mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 230"}},{label:{translate: "mgs.holographic",color:"yellow"},tooltip:{text:"-1 pt"},action:{type:"run_command",command:"/trigger mgs.player.config set 231"}},{label:{translate: "mgs.kobra",color:"yellow"},tooltip:{text:"-1 pt"},action:{type:"run_command",command:"/trigger mgs.player.config set 232"}},{label:{translate: "mgs.acog_red_dot_3x_scope",color:"yellow"},tooltip:{text:"-1 pt"},action:{type:"run_command",command:"/trigger mgs.player.config set 233"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

