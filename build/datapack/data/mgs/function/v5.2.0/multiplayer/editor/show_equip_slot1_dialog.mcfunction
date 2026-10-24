
#> mgs:v5.2.0/multiplayer/editor/show_equip_slot1_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/config/process
#

function mgs:v5.2.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'[{translate:"mgs.loadout_grenade",fallback:"Loadout - Grenade",color:"gold",bold:true}, " 1"]',hint:'{translate:"mgs.choose_a_grenade_for_slot_1_1_pt_none_is_free",fallback:"Choose a grenade for slot 1 (1 pt, None is free)",color:"gray"}',columns:3}
function mgs:v5.2.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.none",fallback:"None",color:"green"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 460"}},{label:{translate:"mgs.frag_grenade",fallback:"Frag Grenade",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 461"}},{label:{translate:"mgs.semtex",fallback:"Semtex",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 462"}},{label:{translate:"mgs.flash",fallback:"Flash",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 463"}},{label:{translate:"mgs.smoke",fallback:"Smoke",color:"yellow"},tooltip:[{text:"-1"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 464"}}]
function mgs:v5.2.0/multiplayer/show_dialog with storage mgs:temp

