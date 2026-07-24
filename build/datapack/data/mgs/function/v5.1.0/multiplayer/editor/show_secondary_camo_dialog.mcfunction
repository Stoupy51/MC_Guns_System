
#> mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/pick_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_secondary_scope
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_secondary_camo",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_camo_free_cosmetic_only",color:"gray"}',columns:2}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.default",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 490"}},{label:{translate:"mgs.autumn",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 491"}},{label:{translate:"mgs.galaxy",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 492"}},{label:{translate:"mgs.gold",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 493"}},{label:{translate:"mgs.red_polymer",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 494"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

