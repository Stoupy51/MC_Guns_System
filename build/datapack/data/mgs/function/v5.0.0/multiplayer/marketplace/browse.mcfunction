
#> mgs:v5.0.0/multiplayer/marketplace/browse
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Initialize dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.marketplace",color:"light_purple",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.browse_public_loadouts_from_all_players",color:"gray"}}],actions:[],columns:1,after_action:"close",exit_action:{label:"Back"}}

# Copy all loadouts for iteration
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts

# Build list recursively (filtered by public:1b)
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/marketplace/build_list

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

