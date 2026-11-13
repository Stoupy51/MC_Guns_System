
#> mgs:v5.4.2/zombies/save/load_row_add
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
#
# @args		n (unknown)
#			name (unknown)
#			map_id (unknown)
#			round (unknown)
#			slot (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{text:"$(n). ",color:"gray"},{text:"$(name)",color:"gold"},{text:"  $(map_id)  Round $(round)",color:"gray"}]}
$data modify storage mgs:temp dialog.actions append value {label:{text:"📂 Load $(n)",color:"green"},tooltip:{translate:"mgs.load_this_save",fallback:"Load this save"},action:{type:"run_command",command:"/function mgs:v5.4.2/dialog/close_then {run:\"zombies/save/load {slot:$(slot)}\"}"}}
$data modify storage mgs:temp dialog.actions append value {label:{text:"🗑 Delete $(n)",color:"red"},tooltip:{translate:"mgs.ask_before_emptying_this_slot",fallback:"Ask before emptying this slot"},action:{type:"run_command",command:"/function mgs:v5.4.2/zombies/save/delete_ask {slot:$(slot)}"}}

