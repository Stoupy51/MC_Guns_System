
#> mgs:v5.3.0/multiplayer/map_select
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.3.0/multiplayer/setup
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🗺 ",{translate:"mgs.select_map",fallback:"Select Map",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_map_to_select_it",fallback:"Click a map to select it",color:"gray"}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",fallback:"Back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup",fallback:"Return to setup"},action:{type:"show_dialog",dialog:"mgs:v5.3.0/multiplayer/setup"}}}

data modify storage mgs:temp _map_iter set from storage mgs:maps multiplayer
scoreboard players set #map_idx mgs.data 0
data modify storage mgs:temp _map_select_mode set value "multiplayer"
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.3.0/shared/maps/select_iter

# multi_action needs at least one action.
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_maps_registered",fallback:"No maps registered",color:"red"},tooltip:{translate:"mgs.create_one_in_the_map_editor_first",fallback:"Create one in the map editor first"},action:{type:"show_dialog",dialog:"mgs:v5.3.0/multiplayer/setup"}}

function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

