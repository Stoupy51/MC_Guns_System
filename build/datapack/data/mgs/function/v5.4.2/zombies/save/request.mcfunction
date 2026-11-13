
#> mgs:v5.4.2/zombies/save/request
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/zombies/save/save_menu {slot:0,name:\"$(name)\"}
#			string in mgs:v5.4.2/zombies/save/save_menu {slot:1,name:\"$(name)\"}
#			string in mgs:v5.4.2/zombies/save/save_menu {slot:2,name:\"$(name)\"}
#			string in mgs:v5.4.2/zombies/save/save_menu {slot:3,name:\"$(name)\"}
#			string in mgs:v5.4.2/zombies/save/save_menu {slot:4,name:\"$(name)\"}
#
# @args		slot (int)
#			name (string)
#

$execute unless data storage mgs:zombies_saves slots[$(slot)].format run return run function mgs:v5.4.2/zombies/save/save {slot:$(slot),name:"$(name)"}

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","Overwrite ","","?"],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.the_running_game_replaces_this_save",fallback:"The running game replaces this save.",color:"gray"}}],actions:[{label:{translate:"mgs.overwrite",fallback:"Overwrite",color:"gold"},tooltip:{translate:"mgs.replace_the_save",fallback:"Replace the save"},action:{type:"run_command",command:"/function mgs:v5.4.2/zombies/save/save {slot:$(slot),name:\"$(name)\"}"}}],columns:1,pause:false,after_action:"close",exit_action:{label:{translate:"mgs.cancel",fallback:"Cancel",color:"gray"}}}
$data modify storage mgs:temp dialog.title[2] set from storage mgs:zombies_saves slots[$(slot)].name
function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

