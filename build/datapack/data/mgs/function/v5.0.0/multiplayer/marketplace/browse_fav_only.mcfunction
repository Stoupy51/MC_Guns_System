
#> mgs:v5.0.0/multiplayer/marketplace/browse_fav_only
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Initialize dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.marketplace",color:"light_purple",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.browse_public_loadouts_from_all_players",color:"gray"}}],actions:[],columns:3,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}}
data modify storage mgs:temp dialog.title set value {translate: "mgs.marketplace_favorites",color:"light_purple",bold:true}

# Add filter/sort buttons (favorites tab active)
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.all",color:"white",bold:true},tooltip:{translate: "mgs.show_all_public_loadouts_your_favorites_first"},action:{type:"run_command",command:"/trigger mgs.player.config set 1600"}}
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.favorites",color:"gold",bold:true},tooltip:{translate: "mgs.show_only_loadouts_you_favorited"},action:{type:"run_command",command:"/trigger mgs.player.config set 1601"}}
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.best_liked",color:"white",bold:true},tooltip:{translate: "mgs.show_all_public_loadouts_sorted_by_most_likes"},action:{type:"run_command",command:"/trigger mgs.player.config set 1602"}}

# Load player favorites
function mgs:v5.0.0/multiplayer/shared/load_player_favorites

# Only show public + in favorites
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/marketplace/build_list_favs

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

