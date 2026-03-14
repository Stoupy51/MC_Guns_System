
#> mgs:v5.0.0/multiplayer/marketplace/browse
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#			mgs:v5.0.0/multiplayer/custom/toggle_favorite
#			mgs:v5.0.0/multiplayer/custom/like
#

# Initialize dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.marketplace",color:"light_purple",bold:true},body:{type:"minecraft:item",item:{id:"minecraft:emerald"},description:{contents:{translate:"mgs.browse_public_loadouts_from_all_players",color:"gray"}},show_decoration:false,show_tooltip:true},actions:[],columns:3,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}}

# Add filter/sort buttons (row 1: all / favorites / best liked)
data modify storage mgs:temp dialog.actions append value {label:[{text:"",color:"aqua",bold:true},"📋 ",{translate:"mgs.all"}],tooltip:{translate:"mgs.show_all_public_loadouts_your_favorites_first"},action:{type:"run_command",command:"/trigger mgs.player.config set 1600"}}
data modify storage mgs:temp dialog.actions append value {label:[{text:"",color:"yellow",bold:true},"⭐ ",{translate:"mgs.favorites"}],tooltip:{translate:"mgs.show_only_loadouts_you_favorited"},action:{type:"run_command",command:"/trigger mgs.player.config set 1601"}}
data modify storage mgs:temp dialog.actions append value {label:[{text:"",color:"white",bold:true},"❤ ",{translate:"mgs.best_liked"}],tooltip:{translate:"mgs.show_all_public_loadouts_sorted_by_most_likes"},action:{type:"run_command",command:"/trigger mgs.player.config set 1602"}}

# Load player favorites
function mgs:v5.0.0/multiplayer/shared/load_player_favorites

# Pass 1: Public loadouts that are in player's favorites
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/marketplace/build_list_favs

# Pass 2: Public loadouts NOT in player's favorites
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/marketplace/build_list_rest

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

