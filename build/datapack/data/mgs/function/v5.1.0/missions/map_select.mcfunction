
#> mgs:v5.1.0/missions/map_select
#
# @within	???
#

# Build the base map-select dialog (empty actions), then append one button per map
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🗺 ",{translate:"mgs.select_mission_map",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_map_to_select_it",color:"gray"}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"show_dialog",dialog:"mgs:v5.1.0/missions/setup"}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage mgs:temp _map_iter set from storage mgs:maps missions
scoreboard players set #map_idx mgs.data 0
data modify storage mgs:temp _map_select_mode set value "missions"
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.1.0/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_mission_maps",color:"red"},tooltip:{translate:"mgs.create_one_in_the_map_editor_first"},action:{type:"show_dialog",dialog:"mgs:v5.1.0/missions/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

