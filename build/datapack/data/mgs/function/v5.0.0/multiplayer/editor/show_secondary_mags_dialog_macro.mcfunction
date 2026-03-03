
#> mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_secondary_magazines",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",{"translate": "mgs.points_remaining","color":"white"},{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate: "mgs.select_number_of_secondary_magazines_1_pt_each",color:"gray"}}],actions:[{label:{translate: "mgs.no_mags_0",color:"green"},tooltip:["",{"translate": "mgs.free","color":"gold"},{"translate": "mgs.no_secondary_magazines","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 396"}},{label:{translate: "mgs.1x_magazine",color:"yellow"},tooltip:["",{"translate": "mgs.1_pt","color":"gold"},{"translate": "mgs.1_magazines_in_inventory","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 397"}},{label:{translate: "mgs.2x_magazine",color:"yellow"},tooltip:["",{"translate": "mgs.2_pt","color":"gold"},{"translate": "mgs.2_magazines_in_inventory","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 398"}},{label:{translate: "mgs.3x_magazine",color:"yellow"},tooltip:["",{"translate": "mgs.3_pt","color":"gold"},{"translate": "mgs.3_magazines_in_inventory","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 399"}},{label:{translate: "mgs.4x_magazine",color:"yellow"},tooltip:["",{"translate": "mgs.4_pt","color":"gold"},{"translate": "mgs.4_magazines_in_inventory","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 400"}},{label:{translate: "mgs.5x_magazine",color:"yellow"},tooltip:["",{"translate": "mgs.5_pt","color":"gold"},{"translate": "mgs.5_magazines_in_inventory","color":"gray"}],action:{type:"run_command",command:"/trigger mgs.player.config set 401"}}],columns:1,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 360"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

