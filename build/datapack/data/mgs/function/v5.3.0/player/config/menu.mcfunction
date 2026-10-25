
#> mgs:v5.3.0/player/config/menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#			mgs:v5.3.0/player/config/toggle_hitmarker
#			mgs:v5.3.0/player/config/toggle_damage_debug
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🎮 ",{translate:"mgs.player_settings",fallback:"Player Settings",color:"gold",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.toggle_your_personal_settings",fallback:"Toggle your personal settings","color":"gray"}}],actions:[],columns:1,after_action:"close",exit_action:{label:{translate:"gui.done"}}}

execute if score @s mgs.player.hitmarker matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.hitmarker_sound",fallback:"Hitmarker Sound: "},{text:"ON ✔",color:"green"}],tooltip:{translate:"mgs.toggle_hitmarker_sound_on_entity_hit",fallback:"Toggle hitmarker sound on entity hit"},action:{type:"run_command",command:"/trigger mgs.player.config set 2"}}
execute unless score @s mgs.player.hitmarker matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.hitmarker_sound",fallback:"Hitmarker Sound: "},[{translate:"mgs.off",fallback:"OFF",color:"red"}, " ✘"]],tooltip:{translate:"mgs.toggle_hitmarker_sound_on_entity_hit",fallback:"Toggle hitmarker sound on entity hit"},action:{type:"run_command",command:"/trigger mgs.player.config set 2"}}

execute if score @s mgs.player.damage_debug matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.damage_debug_2",fallback:"Damage Debug: "},{text:"ON ✔",color:"green"}],tooltip:{translate:"mgs.toggle_damage_numbers_in_chat",fallback:"Toggle damage numbers in chat"},action:{type:"run_command",command:"/trigger mgs.player.config set 3"}}
execute unless score @s mgs.player.damage_debug matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.damage_debug_2",fallback:"Damage Debug: "},[{translate:"mgs.off",fallback:"OFF",color:"red"}, " ✘"]],tooltip:{translate:"mgs.toggle_damage_numbers_in_chat",fallback:"Toggle damage numbers in chat"},action:{type:"run_command",command:"/trigger mgs.player.config set 3"}}

data modify storage mgs:temp dialog.actions append value {label:["","⚔ ",{translate:"mgs.multiplayer_class",fallback:"Multiplayer Class",color:"aqua",bold:true}],tooltip:{translate:"mgs.open_multiplayer_class_selection_menu",fallback:"Open multiplayer class selection menu"},action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}

function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

