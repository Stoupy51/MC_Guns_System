
#> mgs:v5.0.0/multiplayer/editor/scope/primary_full
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_primary
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_scope",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_optic_attachment",color:"gray"}}],actions:[{label:{translate: "mgs.iron_sights",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 230"}},{label:{translate: "mgs.holographic",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 231"}},{label:{translate: "mgs.kobra",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 232"}},{label:{translate: "mgs.acog_red_dot_3x_scope",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 233"}},{label:{translate: "mgs.mk4_4x_scope",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 234"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

