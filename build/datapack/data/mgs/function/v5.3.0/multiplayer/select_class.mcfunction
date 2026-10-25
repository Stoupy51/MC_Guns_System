
#> mgs:v5.3.0/multiplayer/select_class
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/tick
#			mgs:v5.3.0/player/config/process
#			mgs:v5.3.0/multiplayer/start [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.3.0/multiplayer/join_game
#			mgs:v5.3.0/missions/preload_complete [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.3.0/missions/join_game
#			dialog mgs:v5.3.0/multiplayer/setup
#			dialog mgs:v5.3.0/missions/setup
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.select_your_class",fallback:"Select Your Class",color:"gold",bold:true},body:{type:"minecraft:item",item:{id:"minecraft:crossbow"},description:{contents:{translate:"mgs.choose_a_class_for_multiplayer",fallback:"Choose a class for multiplayer",color:"gray"}},show_decoration:false,show_tooltip:true},actions:[],columns:2,after_action:"close",exit_action:{label:"Cancel"}}

data modify storage mgs:temp class_iter set from storage mgs:multiplayer classes_list

execute if data storage mgs:temp class_iter[0] run function mgs:v5.3.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]

data modify storage mgs:temp dialog.actions append value {label:[{text:"✚ ",color:"aqua",bold:true},{translate:"mgs.create_loadout",fallback:"Create Loadout"}],tooltip:{translate:"mgs.build_a_custom_loadout_from_scratch",fallback:"Build a custom loadout from scratch"},action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}
data modify storage mgs:temp dialog.actions append value {label:["","📦 ",{translate:"mgs.my_loadouts",fallback:"My Loadouts",color:"yellow",bold:true}],tooltip:{translate:"mgs.manage_your_custom_loadouts",fallback:"Manage your custom loadouts"},action:{type:"run_command",command:"/trigger mgs.player.config set 102"}}
data modify storage mgs:temp dialog.actions append value {label:["","🌍 ",{translate:"mgs.marketplace",fallback:"Marketplace",color:"light_purple",bold:true}],tooltip:{translate:"mgs.browse_public_loadouts_from_other_players",fallback:"Browse public loadouts from other players"},action:{type:"run_command",command:"/trigger mgs.player.config set 101"}}

function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

