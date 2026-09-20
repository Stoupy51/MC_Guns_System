
#> mgs:v5.1.0/multiplayer/editor/show_knife_camo_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

function mgs:v5.1.0/multiplayer/editor/recompute_points
data modify storage mgs:temp _dlg merge value {title:'{translate:"mgs.loadout_knife_camo",color:"gold",bold:true}',hint:'{translate:"mgs.choose_your_camo_free_cosmetic_only",color:"gray"}',columns:2}
function mgs:v5.1.0/multiplayer/editor/show_static_dialog with storage mgs:temp _dlg
data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.default",color:"green"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 600"}},{label:{translate:"mgs.autumn",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 601"}},{label:{translate:"mgs.galaxy",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 602"}},{label:{translate:"mgs.gold",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 603"}},{label:{translate:"mgs.red_polymer",color:"yellow"},tooltip:{translate:"mgs.free"},action:{type:"run_command",command:"/trigger mgs.player.config set 604"}}]
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

