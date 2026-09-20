
#> mgs:v5.1.0/multiplayer/editor/show_secondary_pistol_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/show_secondary_dialog
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_secondary_weapon",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_secondary_weapon_1_pt_1_pt_per_magazine",color:"gray"}',columns:2}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{text:"M1911",color:"yellow"},tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 250"}},{label:{text:"M9",color:"yellow"},tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 251"}},{label:{translate:"mgs.deagle",color:"yellow"},tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 252"}},{label:{translate:"mgs.makarov",color:"yellow"},tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 253"}},{label:[{translate:"mgs.glock",color:"yellow"}, " 17"],tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 254"}},{label:[{translate:"mgs.glock",color:"yellow"}, " 18"],tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 255"}},{label:{text:"VZ-61",color:"yellow"},tooltip:["",{"translate":"mgs.pistol","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 256"}},{label:["","\ud83d\uddd1 ",{translate:"mgs.remove_secondary",color:"red"}],tooltip:{translate:"mgs.clear_the_secondary_weapon_refunds_its_points"},action:{type:"run_command",command:"/trigger mgs.player.config set 112"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

