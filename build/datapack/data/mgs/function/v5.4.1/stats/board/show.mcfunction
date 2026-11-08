
#> mgs:v5.4.1/stats/board/show
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/board/dispatch {path:"level_mp",kind:"level_mp",title:"Multiplayer Level",filters:0b}
#			mgs:v5.4.1/stats/board/dispatch {path:"level_zb",kind:"level_zb",title:"Zombies Level",filters:0b}
#			mgs:v5.4.1/stats/board/zb_map_path with storage mgs:temp _lb_view
#			mgs:v5.4.1/stats/board/mi_map_path with storage mgs:temp _lb_view
#
# @args		path (string)
#			kind (string)
#			title (string)
#			filters (byte)
#

$function mgs:v5.4.1/stats/board/render {path:'$(path)',kind:"$(kind)"}
$data modify storage mgs:temp dialog set value {type:"minecraft:notice",title:["","🏆 ",{text:"$(title)",color:"gold",bold:true}],body:[{type:"minecraft:plain_message",width:300,contents:[""]},{type:"minecraft:plain_message",width:300,contents:[""]}],pause:false,after_action:"none",action:{"label": {"translate": "gui.done"}, "action": {"type": "run_command", "command": "/trigger mgs.player.config set 1640"}}}
data modify storage mgs:temp dialog.body[1].contents append from storage mgs:temp _lb_lines[]
execute unless data storage mgs:temp _lb_lines[0] run data modify storage mgs:temp dialog.body[1].contents append value {translate:"mgs.no_entries_yet",fallback:"No entries yet",color:"gray"}

$data modify storage mgs:temp _lb_walk set from storage mgs:stats leaderboards.$(path)
data modify storage mgs:temp _lb_me set from entity @s UUID
scoreboard players set #lb_k mgs.data 1
execute store success score #lb_found mgs.data run function mgs:v5.4.1/stats/board/find_me
execute if score #lb_found mgs.data matches 1 store result storage mgs:temp _lb_rank.k int 1 run scoreboard players get #lb_k mgs.data
execute if score #lb_found mgs.data matches 1 run function mgs:v5.4.1/stats/board/show_rank with storage mgs:temp _lb_rank

$data modify storage mgs:temp _lb_f set value $(filters)
execute if data storage mgs:temp {_lb_f:1} run function mgs:v5.4.1/stats/board/filters with storage mgs:temp _lb_view
data modify storage mgs:temp dialog.body[0].contents append value [{"text": "[", "color": "gray", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 1630"}}, "Back", "]"]
function mgs:v5.4.1/multiplayer/show_dialog with storage mgs:temp

