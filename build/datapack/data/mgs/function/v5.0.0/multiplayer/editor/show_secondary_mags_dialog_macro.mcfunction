
#> mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.create_loadout_secondary_magazines",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{translate:"mgs.select_number_of_secondary_magazines_1_pt_each",color:"gray"}}],actions:[{label:[{translate:"mgs.no_mags",color:"green"}, " (0)"],tooltip:["",{translate:"mgs.free","color":"gold"},[{"text":"\n","color":"gray"}, {"translate":"mgs.no_secondary_magazines"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 396"}},{label:[{text:"1",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",[{text:"-1","color":"gold"}, " pt"],[{"text":"\n1 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 397"}},{label:[{text:"2",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",[{text:"-2","color":"gold"}, " pt"],[{"text":"\n2 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 398"}},{label:[{text:"3",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",[{text:"-3","color":"gold"}, " pt"],[{"text":"\n3 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 399"}},{label:[{text:"4",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",[{text:"-4","color":"gold"}, " pt"],[{"text":"\n4 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 400"}},{label:[{text:"5",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",[{text:"-5","color":"gold"}, " pt"],[{"text":"\n5 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 401"}}],columns:1,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 360"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

