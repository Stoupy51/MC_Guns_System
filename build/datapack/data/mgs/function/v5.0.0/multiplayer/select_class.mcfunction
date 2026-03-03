
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

# Show the completed dialog via macro
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

