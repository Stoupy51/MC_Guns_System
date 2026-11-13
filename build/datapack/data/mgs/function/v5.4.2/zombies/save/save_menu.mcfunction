
#> mgs:v5.4.2/zombies/save/save_menu
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/zombies/admin
#

execute unless score #zb_next_round mgs.data matches 1.. run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.a_game_can_only_be_saved_between_two_rounds","fallback":"A game can only be saved between two rounds.","color":"red"}]

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","💾 ",{translate:"mgs.save_quit",fallback:"Save & Quit",color:"gold",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.name_the_save_and_pick_a_slot_the_game_stops_once_saved",fallback:"Name the save and pick a slot. The game stops once saved.",color:"gray"}}],inputs:[{type:"minecraft:text",key:"name",label:"Save name",initial:"",max_length:32}],actions:[],columns:1,pause:false,after_action:"close",exit_action:{label:{translate:"mgs.cancel",fallback:"Cancel",color:"gray"}}}

data modify storage mgs:temp dialog.actions append value {label:["","Slot 1: ",{translate:"mgs.empty",fallback:"Empty",color:"gray"}],tooltip:{translate:"mgs.save_the_running_game_in_this_slot",fallback:"Save the running game in this slot"},action:{type:"minecraft:dynamic/run_command",template:"/function mgs:v5.4.2/zombies/save/request {slot:0,name:\"$(name)\"}"}}
execute if data storage mgs:zombies_saves slots[0].name run data modify storage mgs:temp dialog.actions[0].label[2] set from storage mgs:zombies_saves slots[0].name

data modify storage mgs:temp dialog.actions append value {label:["","Slot 2: ",{translate:"mgs.empty",fallback:"Empty",color:"gray"}],tooltip:{translate:"mgs.save_the_running_game_in_this_slot",fallback:"Save the running game in this slot"},action:{type:"minecraft:dynamic/run_command",template:"/function mgs:v5.4.2/zombies/save/request {slot:1,name:\"$(name)\"}"}}
execute if data storage mgs:zombies_saves slots[1].name run data modify storage mgs:temp dialog.actions[1].label[2] set from storage mgs:zombies_saves slots[1].name

data modify storage mgs:temp dialog.actions append value {label:["","Slot 3: ",{translate:"mgs.empty",fallback:"Empty",color:"gray"}],tooltip:{translate:"mgs.save_the_running_game_in_this_slot",fallback:"Save the running game in this slot"},action:{type:"minecraft:dynamic/run_command",template:"/function mgs:v5.4.2/zombies/save/request {slot:2,name:\"$(name)\"}"}}
execute if data storage mgs:zombies_saves slots[2].name run data modify storage mgs:temp dialog.actions[2].label[2] set from storage mgs:zombies_saves slots[2].name

data modify storage mgs:temp dialog.actions append value {label:["","Slot 4: ",{translate:"mgs.empty",fallback:"Empty",color:"gray"}],tooltip:{translate:"mgs.save_the_running_game_in_this_slot",fallback:"Save the running game in this slot"},action:{type:"minecraft:dynamic/run_command",template:"/function mgs:v5.4.2/zombies/save/request {slot:3,name:\"$(name)\"}"}}
execute if data storage mgs:zombies_saves slots[3].name run data modify storage mgs:temp dialog.actions[3].label[2] set from storage mgs:zombies_saves slots[3].name

data modify storage mgs:temp dialog.actions append value {label:["","Slot 5: ",{translate:"mgs.empty",fallback:"Empty",color:"gray"}],tooltip:{translate:"mgs.save_the_running_game_in_this_slot",fallback:"Save the running game in this slot"},action:{type:"minecraft:dynamic/run_command",template:"/function mgs:v5.4.2/zombies/save/request {slot:4,name:\"$(name)\"}"}}
execute if data storage mgs:zombies_saves slots[4].name run data modify storage mgs:temp dialog.actions[4].label[2] set from storage mgs:zombies_saves slots[4].name

data modify storage mgs:temp _sv_name set value {}
data modify storage mgs:temp _sv_name.map_id set from storage mgs:zombies game.map_id
execute store result storage mgs:temp _sv_name.round int 1 run data get storage mgs:zombies game.round
function mgs:v5.4.2/zombies/save/menu_name with storage mgs:temp _sv_name

function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

