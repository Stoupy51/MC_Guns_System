
#> mgs:v5.0.0/multiplayer/my_loadouts/browse
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Initialize dialog with 2 columns: [Use][Delete] per loadout
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.my_loadouts",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.select_a_loadout_to_use_or_delete_it",color:"gray"}}],actions:[],columns:2,after_action:"close",exit_action:{label:"Back"}}

# Copy all loadouts for iteration
data modify storage mgs:temp _iter set from storage mgs:multiplayer custom_loadouts

# Build list recursively (filtered by owner_pid via score comparison)
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/my_loadouts/build_list

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

