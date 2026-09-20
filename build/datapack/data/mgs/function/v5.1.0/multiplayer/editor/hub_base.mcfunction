
#> mgs:v5.1.0/multiplayer/editor/hub_base
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp _hub
#
# @args		used (unknown)
#			pts (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.loadout",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_used"},": "],{"text":"$(used)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"},{"text":" ($(pts) left)","color":"gray"}]},{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_category_to_change_it",color:"gray"}}],actions:[],columns:2,after_action:"close",exit_action:{label:"Cancel",action:{type:"run_command",command:"/trigger mgs.player.config set 4"}}}

