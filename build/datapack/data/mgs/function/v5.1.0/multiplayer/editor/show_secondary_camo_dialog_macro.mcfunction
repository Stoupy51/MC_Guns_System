
#> mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.loadout_secondary_camo",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate:"mgs.choose_your_camo_free_cosmetic_only",color:"gray"}}],actions:[{label:{translate:"mgs.default",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 490"}},{label:{translate:"mgs.autumn",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 491"}},{label:{translate:"mgs.galaxy",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 492"}},{label:{translate:"mgs.gold",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 493"}},{label:{translate:"mgs.red_polymer",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 494"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}}
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

