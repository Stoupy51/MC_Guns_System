
#> mgs:v5.4.2/zombies/save/load_menu
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/delete
#			string in mgs:v5.4.2/zombies/save/delete_ask
#			dialog mgs:v5.4.2/zombies/setup
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","📂 ",{translate:"mgs.load_save",fallback:"Load Save",color:"gold",bold:true}],body:[],actions:[],columns:2,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",fallback:"Back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup",fallback:"Return to setup"},action:{type:"show_dialog",dialog:"mgs:v5.4.2/zombies/setup"}}}

data modify storage mgs:temp _sv_row set value {slot:0,n:1}
execute if data storage mgs:zombies_saves slots[0].format run function mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
execute unless data storage mgs:zombies_saves slots[0].format run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:[{text:"1. ",color:"gray"}, {translate:"mgs.empty",fallback:"Empty"}]}

data modify storage mgs:temp _sv_row set value {slot:1,n:2}
execute if data storage mgs:zombies_saves slots[1].format run function mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
execute unless data storage mgs:zombies_saves slots[1].format run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:[{text:"2. ",color:"gray"}, {translate:"mgs.empty",fallback:"Empty"}]}

data modify storage mgs:temp _sv_row set value {slot:2,n:3}
execute if data storage mgs:zombies_saves slots[2].format run function mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
execute unless data storage mgs:zombies_saves slots[2].format run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:[{text:"3. ",color:"gray"}, {translate:"mgs.empty",fallback:"Empty"}]}

data modify storage mgs:temp _sv_row set value {slot:3,n:4}
execute if data storage mgs:zombies_saves slots[3].format run function mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
execute unless data storage mgs:zombies_saves slots[3].format run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:[{text:"4. ",color:"gray"}, {translate:"mgs.empty",fallback:"Empty"}]}

data modify storage mgs:temp _sv_row set value {slot:4,n:5}
execute if data storage mgs:zombies_saves slots[4].format run function mgs:v5.4.2/zombies/save/load_row with storage mgs:temp _sv_row
execute unless data storage mgs:zombies_saves slots[4].format run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:[{text:"5. ",color:"gray"}, {translate:"mgs.empty",fallback:"Empty"}]}

execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_saves_yet",fallback:"No saves yet",color:"red"},tooltip:{translate:"mgs.save_a_running_game_between_two_rounds_from_the_admin_menu",fallback:"Save a running game between two rounds from the admin menu"},action:{type:"show_dialog",dialog:"mgs:v5.4.2/zombies/setup"}}

function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

