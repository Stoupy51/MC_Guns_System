
#> mgs:v5.3.0/stats/board/filters_add
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/filters with storage mgs:temp _lb_view
#
# @args		f0 (unknown)
#			f1 (unknown)
#			f2 (unknown)
#			f3 (unknown)
#			f4 (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.all",fallback:"All",color:"aqua"},action:{type:"run_command",command:"/trigger mgs.player.config set $(f0)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"1 ",color:"aqua"}, {translate:"mgs.player",fallback:"player"}],action:{type:"run_command",command:"/trigger mgs.player.config set $(f1)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"2 ",color:"aqua"}, {translate:"mgs.players_3",fallback:"players"}],action:{type:"run_command",command:"/trigger mgs.player.config set $(f2)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"3 ",color:"aqua"}, {translate:"mgs.players_3",fallback:"players"}],action:{type:"run_command",command:"/trigger mgs.player.config set $(f3)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"4 ",color:"aqua"}, {translate:"mgs.players_3",fallback:"players"}],action:{type:"run_command",command:"/trigger mgs.player.config set $(f4)"}}

