
#> mgs:v5.4.1/stats/board/maps
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/board/dispatch {mode:"zombies",base:3000,step:8}
#			mgs:v5.4.1/stats/board/dispatch {mode:"missions",base:2000,step:1}
#
# @args		mode (string)
#			base (int)
#			step (int)
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🏆 ",{translate:"mgs.pick_a_map",fallback:"Pick a map",color:"gold",bold:true}],actions:[],columns:2,pause:false,after_action:"none",exit_action:{"label": {"translate": "gui.done"}, "action": {"type": "run_command", "command": "/trigger mgs.player.config set 1640"}}}
$data modify storage mgs:temp _lb_maps set from storage mgs:maps $(mode)
$scoreboard players set #lb_t mgs.data $(base)
$scoreboard players set #lb_step mgs.data $(step)
function mgs:v5.4.1/stats/board/maps_next
data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.back",fallback:"Back",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set 1630"}}
function mgs:v5.4.1/multiplayer/show_dialog with storage mgs:temp

