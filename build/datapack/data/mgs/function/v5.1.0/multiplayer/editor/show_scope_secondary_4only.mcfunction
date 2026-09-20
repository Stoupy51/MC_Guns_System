
#> mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/pick_secondary
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_secondary_scope",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_secondary_optic_1_pt_for_scope_iron_sights_free",color:"gray"}',columns:2}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.iron_sights",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 260"}},{label:{translate:"mgs.mk4_4x_scope",color:"yellow"},tooltip:[{text:"-1","color":"gold"}, " pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 264"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

