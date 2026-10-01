
#> mgs:v5.1.0/players/list_missions
#
# @executed	as the player & at current position
#
# @within	string in mgs:v5.1.0/players/row_missions
#			dialog mgs:v5.1.0/missions/setup
#

# The mode is set first, so append_self can colour by status.
data modify storage mgs:temp _plr_mode set value "missions"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# One row per player; stays open after a pick, Back returns to setup.
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.manage_players",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.one_row_per_player_click_a_name_to_refresh",color:"gray"}}],actions:[],columns:3,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}}

execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# multi_action needs at least one action.
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}

function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

