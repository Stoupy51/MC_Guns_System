
#> mgs:v5.0.0/multiplayer/editor/show_perks_dialog_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_perks_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#			_perk_count (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.create_loadout_perks",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{text:"Toggle perks below (max 3, 1 pt each). Selected: $(_perk_count)/3",color:"gray"}},{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_perk_to_toggle_currently_selected_perks_are_removed_for_",color:"dark_gray"}}],actions:[{label:{translate:"mgs.sleight_of_hand",color:"aqua"},tooltip:["",{"translate":"mgs.reload_50_faster","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 410"}},{label:{translate:"mgs.fast_hands",color:"aqua"},tooltip:["",{"translate":"mgs.swap_weapons_50_faster","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 411"}},{label:{translate:"mgs.overkill",color:"aqua"},tooltip:["",{"translate":"mgs.unlimited_ammo_for_30s_on_spawn","color":"gray"},["","\n",{"translate":"mgs.cost"},": "],[{"text":"1","color":"gold"}]," pt"],action:{type:"run_command",command:"/trigger mgs.player.config set 412"}},{label:{translate:"mgs.done_confirm",color:"green","bold":true},tooltip:{translate:"mgs.finish_perks_and_review_loadout_free_action"},action:{type:"run_command",command:"/trigger mgs.player.config set 450"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 370"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

