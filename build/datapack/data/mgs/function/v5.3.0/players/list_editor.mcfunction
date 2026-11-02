
#> mgs:v5.3.0/players/list_editor
#
# @within	string in mgs:v5.3.0/players/row_editor
#			string in mgs:v5.3.0/maps/editor/enter
#

execute unless score @s mgs.mp.map_edit matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_must_be_in_map_editor_to_invite_players","fallback":"You must be in map editor to invite players.","color":"red"}]

data modify storage mgs:temp _plr_mode set value "editor"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.3.0/players/append_self

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.invite_to_the_editor",fallback:"Invite to the Editor",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.green_players_already_edit_this_map_click_a_name_to_refresh",fallback:"Green players already edit this map. Click a name to refresh.",color:"gray"}}],actions:[],columns:2,pause:false,after_action:"none",exit_action:{label:{translate:"mgs.close",fallback:"Close",color:"gray"}}}
function mgs:v5.3.0/players/list_iter
data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.everyone",fallback:"Everyone",color:"aqua"},tooltip:{translate:"mgs.invite_every_online_player",fallback:"Invite every online player"},action:{type:"run_command",command:"/function mgs:v5.3.0/maps/editor/invite_all"}}
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

