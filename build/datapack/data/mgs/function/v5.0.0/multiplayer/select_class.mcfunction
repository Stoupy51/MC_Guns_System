
#> mgs:v5.0.0/multiplayer/select_class
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#			mgs:v5.0.0/multiplayer/start [ as @a & at @s ]
#

# Initialize dialog structure
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.select_your_class",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_a_class_for_multiplayer",color:"gray"}}],actions:[],columns:2,after_action:"close",exit_action:{label:"Cancel"}}

# Copy class list for iteration
data modify storage mgs:temp class_iter set from storage mgs:multiplayer classes_list

# Build dialog actions recursively (passes first class data as macro args)
execute if data storage mgs:temp class_iter[0] run function mgs:v5.0.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]

# Append custom loadout buttons
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.create_loadout",color:"aqua",bold:true},tooltip:{translate: "mgs.build_a_custom_loadout_from_scratch"},action:{type:"run_command",command:"/trigger mgs.player.config set 100"}}
data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.my_loadouts",color:"yellow",bold:true},tooltip:{translate: "mgs.manage_your_custom_loadouts"},action:{type:"run_command",command:"/trigger mgs.player.config set 102"}}
data modify storage mgs:temp dialog.actions append value {label:{text:"🌍 Marketplace",color:"light_purple",bold:true},tooltip:{translate: "mgs.browse_public_loadouts_from_other_players"},action:{type:"run_command",command:"/trigger mgs.player.config set 101"}}

# Show the completed dialog via macro
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

