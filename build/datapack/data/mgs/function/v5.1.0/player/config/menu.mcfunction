
#> mgs:v5.1.0/player/config/menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#			mgs:v5.1.0/player/config/toggle_hitmarker
#			mgs:v5.1.0/player/config/toggle_damage_debug
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🎮 ",{translate:"mgs.player_settings",color:"gold",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.toggle_your_personal_settings","color":"gray"}}],actions:[],columns:1,after_action:"close",exit_action:{label:{translate:"gui.done"}}}

execute if score @s mgs.player.hitmarker matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.hitmarker_sound"},{text:"ON ✔",color:"green"}],tooltip:{translate:"mgs.toggle_hitmarker_sound_on_entity_hit"},action:{type:"run_command",command:"/trigger mgs.player.config set 2"}}
execute unless score @s mgs.player.hitmarker matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.hitmarker_sound"},[{translate:"mgs.off",color:"red"}, " ✘"]],tooltip:{translate:"mgs.toggle_hitmarker_sound_on_entity_hit"},action:{type:"run_command",command:"/trigger mgs.player.config set 2"}}

execute if score @s mgs.player.damage_debug matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.damage_debug_2"},{text:"ON ✔",color:"green"}],tooltip:{translate:"mgs.toggle_damage_numbers_in_chat"},action:{type:"run_command",command:"/trigger mgs.player.config set 3"}}
execute unless score @s mgs.player.damage_debug matches 1 run data modify storage mgs:temp dialog.actions append value {label:["",{translate:"mgs.damage_debug_2"},[{translate:"mgs.off",color:"red"}, " ✘"]],tooltip:{translate:"mgs.toggle_damage_numbers_in_chat"},action:{type:"run_command",command:"/trigger mgs.player.config set 3"}}

data modify storage mgs:temp dialog.actions append value {label:["","⚔ ",{translate:"mgs.multiplayer_class",color:"aqua",bold:true}],tooltip:{translate:"mgs.open_multiplayer_class_selection_menu"},action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}

function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

