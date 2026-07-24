
#> mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

execute if data storage mgs:temp editor{primary:""} run return run function mgs:v5.1.0/multiplayer/editor/hub
function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_primary_magazines",color:"gold",bold:true}',hint:'{translate:"mgs.select_the_number_of_magazines_1_pt_each",color:"gray"}',columns:1}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:[{text:"1",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-1","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n1 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 391"}},{label:[{text:"2",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-2","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n2 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 392"}},{label:[{text:"3",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-3","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n3 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 393"}},{label:[{text:"4",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-4","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n4 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 394"}},{label:[{text:"5",color:"yellow"}, {translate:"mgs.x_magazine"}],tooltip:["",{"text":"-5","color":"gold"}," ",{"text":"pt","color":"gold"},[{"text":"\n5 ","color":"gray"}, {"translate":"mgs.magazines_in_inventory"}]],action:{type:"run_command",command:"/trigger mgs.player.config set 395"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

