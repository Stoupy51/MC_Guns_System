
#> mgs:v5.0.0/multiplayer/editor/show_secondary_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_primary
#			mgs:v5.0.0/multiplayer/editor/pick_primary_scope
#

scoreboard players set @s mgs.mp.edit_step 2

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_secondary",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_secondary_weapon_or_skip",color:"gray"}}],actions:[{label:{translate: "mgs.m1911",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 250"}},{label:{text:"M9",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 251"}},{label:{translate: "mgs.deagle",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 252"}},{label:{translate: "mgs.makarov",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 253"}},{label:{translate: "mgs.glock_17",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 254"}},{label:{translate: "mgs.glock_18",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 255"}},{label:{translate: "mgs.vz_61",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 256"}},{label:{translate: "mgs.no_secondary",color:"red"},tooltip:{translate: "mgs.skip_secondary_weapon"},action:{type:"run_command",command:"/trigger mgs.player.config set 258"}}],columns:2,after_action:"close",exit_action:{label:"Cancel"}}
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

