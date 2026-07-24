
#> mgs:v5.1.0/zombies/map_select
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/zombies/setup
#

# Build the base map-select dialog (empty actions), then append one button per map
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🗺 ",{translate:"mgs.select_zombies_map",color:"dark_green",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_map_to_select_it",color:"gray"}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"show_dialog",dialog:"mgs:v5.1.0/zombies/setup"}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage mgs:temp _map_iter set from storage mgs:maps zombies
scoreboard players set #map_idx mgs.data 0
data modify storage mgs:temp _map_select_mode set value "zombies"
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.1.0/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_zombies_maps",color:"red"},tooltip:{translate:"mgs.create_one_in_the_map_editor_first"},action:{type:"show_dialog",dialog:"mgs:v5.1.0/zombies/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

