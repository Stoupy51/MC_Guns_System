
#> mgs:v5.3.0/multiplayer/marketplace/browse_likes
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.marketplace",fallback:"Marketplace",color:"light_purple",bold:true},body:{type:"minecraft:item",item:{id:"minecraft:emerald"},description:{contents:{translate:"mgs.browse_public_loadouts_from_all_players",fallback:"Browse public loadouts from all players",color:"gray"}},show_decoration:false,show_tooltip:true},actions:[],columns:3,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}}
data modify storage mgs:temp dialog.title set value [{text:"",color:"light_purple",bold:true},{translate:"mgs.marketplace",fallback:"Marketplace"}," — ",{translate:"mgs.best_liked",fallback:"Best Liked"}]

data modify storage mgs:temp dialog.actions append value {label:["","📋 ",{translate:"mgs.all",fallback:"All",color:"white",bold:true}],tooltip:{translate:"mgs.show_all_public_loadouts_your_favorites_first",fallback:"Show all public loadouts (your favorites first)"},action:{type:"run_command",command:"/trigger mgs.player.config set 1600"}}
data modify storage mgs:temp dialog.actions append value {label:["","⭐ ",{translate:"mgs.favorites",fallback:"Favorites",color:"yellow",bold:true}],tooltip:{translate:"mgs.show_only_loadouts_you_favorited",fallback:"Show only loadouts you favorited"},action:{type:"run_command",command:"/trigger mgs.player.config set 1601"}}
data modify storage mgs:temp dialog.actions append value {label:["","❤ ",{translate:"mgs.best_liked",fallback:"Best Liked",color:"red",bold:true}],tooltip:{translate:"mgs.show_all_public_loadouts_sorted_by_most_likes",fallback:"Show all public loadouts sorted by most likes"},action:{type:"run_command",command:"/trigger mgs.player.config set 1602"}}

# prep_btn reads them.
function mgs:v5.3.0/multiplayer/shared/load_player_favorites

data modify storage mgs:temp _sort_pool set value []
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _iter[0] run function mgs:v5.3.0/multiplayer/marketplace/sort_collect_pool

execute if data storage mgs:temp _sort_pool[0] run function mgs:v5.3.0/multiplayer/marketplace/sort_build_list

function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

