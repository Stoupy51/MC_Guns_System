
#> mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'[{translate:"mgs.loadout_grenade",color:"gold",bold:true}, " 2"]',hint:'{translate:"mgs.choose_a_grenade_for_slot_2_1_pt_none_is_free",color:"gray"}',columns:3}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.none",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 470"}},{label:{translate:"mgs.frag_grenade",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 471"}},{label:{translate:"mgs.semtex",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 472"}},{label:{translate:"mgs.flash",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 473"}},{label:{translate:"mgs.smoke",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 474"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

