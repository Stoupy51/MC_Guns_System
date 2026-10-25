
#> mgs:v5.3.0/multiplayer/editor/show_scope_primary_1only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/multiplayer/editor/pick_primary
#

function mgs:v5.3.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_primary_scope",fallback:"Loadout - Primary Scope",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_optic_1_pt_for_any_scope_iron_sights_free",fallback:"Choose your optic (-1 pt for any scope, iron sights free)",color:"gray"}',columns:2}
function mgs:v5.3.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.iron_sights",fallback:"Iron Sights",color:"green"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 230"}},{label:{translate:"mgs.holographic",fallback:"Holographic",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 231"}}]
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

