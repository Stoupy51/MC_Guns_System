
#> mgs:v5.4.2/stats/admin/boards
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/config
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.reset_a_map_leaderboard",fallback:"Reset a Map Leaderboard",color:"red",bold:true},actions:[],columns:2,exit_action:{label:{translate:"gui.done"}}}
data modify storage mgs:temp _lb_maps set from storage mgs:maps zombies
function mgs:v5.4.2/stats/board/admin_next {board:"zb_map",label:"Zombies"}
data modify storage mgs:temp _lb_maps set from storage mgs:maps missions
function mgs:v5.4.2/stats/board/admin_next {board:"mi_map",label:"Missions"}
function mgs:v5.4.2/multiplayer/show_dialog with storage mgs:temp

