
#> mgs:v5.0.0/multiplayer/editor/show_equipment_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_secondary
#			mgs:v5.0.0/multiplayer/editor/pick_secondary_scope
#

scoreboard players set @s mgs.mp.edit_step 3

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_equipment",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_equipment_loadout",color:"gray"}}],actions:[{label:{translate: "mgs.2x_frag_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 300"}},{label:{translate: "mgs.2x_semtex",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 301"}},{label:{translate: "mgs.2x_flash_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 302"}},{label:{translate: "mgs.2x_smoke_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 303"}},{label:{translate: "mgs.frag_flash",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 304"}},{label:{translate: "mgs.frag_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 305"}},{label:{translate: "mgs.semtex_flash",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 306"}},{label:{translate: "mgs.semtex_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 307"}},{label:{translate: "mgs.flash_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 308"}},{label:{translate: "mgs.no_equipment",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 309"}}],columns:2,after_action:"close",exit_action:{label:"Cancel"}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

