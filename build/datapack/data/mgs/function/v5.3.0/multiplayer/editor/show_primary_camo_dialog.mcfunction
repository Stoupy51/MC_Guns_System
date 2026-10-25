
#> mgs:v5.3.0/multiplayer/editor/show_primary_camo_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/multiplayer/editor/pick_primary
#			mgs:v5.3.0/multiplayer/editor/pick_primary_scope
#

function mgs:v5.3.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_primary_camo",fallback:"Loadout - Primary Camo",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_camo_free_cosmetic_only",fallback:"Choose your camo (free, cosmetic only)",color:"gray"}',columns:2}
function mgs:v5.3.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.default",fallback:"Default",color:"green"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 480"}},{label:{translate:"mgs.autumn",fallback:"Autumn",color:"yellow"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 481"}},{label:{translate:"mgs.galaxy",fallback:"Galaxy",color:"yellow"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 482"}},{label:{translate:"mgs.gold",fallback:"Gold",color:"yellow"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 483"}},{label:{translate:"mgs.red_polymer",fallback:"Red Polymer",color:"yellow"},tooltip:{translate:"mgs.free",fallback:"Free"},action:{type:"run_command",command:"/trigger mgs.player.config set 484"}}]
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

