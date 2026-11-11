
#> mgs:v5.4.2/multiplayer/editor/show_scope_primary_1only
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/editor/pick_primary
#

function mgs:v5.4.2/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_primary_scope",fallback:"Loadout - Primary Scope",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_optic_1_pt_for_any_scope_iron_sights_free",fallback:"Choose your optic (-1 pt for any scope, iron sights free)",color:"gray"}',columns:2}
function mgs:v5.4.2/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.iron_sights",fallback:"Iron Sights",color:"green"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 230"}},{label:{translate:"mgs.pu_scope_4x",fallback:"PU Scope (4x)",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 231"}}]
function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

