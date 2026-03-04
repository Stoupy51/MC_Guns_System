
#> mgs:v5.0.0/multiplayer/my_loadouts/browse_fav_only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Initialize dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.my_loadouts",color:"gold",bold:true},body:{type:"minecraft:item",item:{id:"minecraft:written_book"},description:{contents:{translate: "mgs.manage_your_custom_loadouts",color:"gray"}},show_decoration:false,show_tooltip:true},actions:[],columns:3,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}}
data modify storage mgs:temp dialog.title set value {translate: "mgs.my_loadouts_favorites",color:"gold",bold:true}

# Add filter/sort buttons (favorites tab active)
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.favorites",color:"gold",bold:true},tooltip:{translate: "mgs.show_only_your_favorited_loadouts"},action:{type:"run_command",command:"/trigger mgs.player.config set 1603"}}
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.all",color:"white",bold:true},tooltip:{translate: "mgs.show_all_your_loadouts_favorites_first_then_private_then_public"},action:{type:"run_command",command:"/trigger mgs.player.config set 102"}}
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.create",color:"green",bold:true},tooltip:{translate: "mgs.build_a_new_custom_loadout_from_scratch"},action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}

# Load player favorites
function mgs:v5.0.0/multiplayer/shared/load_player_favorites

# Only show own loadouts that are in favorites
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/my_loadouts/build_list_favs

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

