
#> mgs:v5.0.0/multiplayer/editor/scope/secondary_4only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_secondary
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_scope_secondary",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_secondary_optic",color:"gray"}}],actions:[{label:{translate: "mgs.iron_sights",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 260"}},{label:{translate: "mgs.mk4_4x_scope",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 264"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 360"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

