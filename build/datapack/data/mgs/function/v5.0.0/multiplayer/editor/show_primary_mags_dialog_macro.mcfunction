
#> mgs:v5.0.0/multiplayer/editor/show_primary_mags_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_primary_mags_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.create_loadout_primary_magazines",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate:"mgs.select_number_of_primary_magazines_1_pt_each",color:"gray"}}],actions:[{label:[{text:"1",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-1","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n1 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 391"}},{label:[{text:"2",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-2","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n2 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 392"}},{label:[{text:"3",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-3","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n3 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 393"}},{label:[{text:"4",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-4","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n4 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 394"}},{label:[{text:"5",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-5","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n5 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 395"}}],columns:1,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

