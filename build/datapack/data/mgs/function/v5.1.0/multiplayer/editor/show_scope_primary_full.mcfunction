
#> mgs:v5.1.0/multiplayer/editor/show_scope_primary_full
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/pick_primary
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_primary_scope",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_optic_1_pt_for_any_scope_iron_sights_free",color:"gray"}',columns:2}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.iron_sights",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 230"}},{label:{translate:"mgs.holographic",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 231"}},{label:{translate:"mgs.kobra",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 232"}},{label:{translate:"mgs.acog_red_dot_3x_scope",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 233"}},{label:{translate:"mgs.mk4_4x_scope",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 234"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

