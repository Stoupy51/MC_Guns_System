
#> mgs:v5.4.2/zombies/save/delete_ask
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/zombies/save/load_row_add {slot:$(slot)}
#
# @args		slot (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","Delete ","","?"],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.the_slot_is_emptied_for_good",fallback:"The slot is emptied for good.",color:"gray"}}],actions:[{label:{translate:"mgs.delete",fallback:"Delete",color:"red"},tooltip:{translate:"mgs.empty_the_slot",fallback:"Empty the slot"},action:{type:"run_command",command:"/function mgs:v5.4.2/zombies/save/delete {slot:$(slot)}"}}],columns:1,pause:false,after_action:"close",exit_action:{label:{translate:"mgs.cancel",fallback:"Cancel",color:"gray"},action:{type:"run_command",command:"/function mgs:v5.4.2/zombies/save/load_menu"}}}
$data modify storage mgs:temp dialog.title[2] set from storage mgs:zombies_saves slots[$(slot)].name
function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

