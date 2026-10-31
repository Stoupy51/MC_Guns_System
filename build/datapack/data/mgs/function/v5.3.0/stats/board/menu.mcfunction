
#> mgs:v5.3.0/stats/board/menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/dispatch
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🏆 ",{translate:"mgs.leaderboards",fallback:"Leaderboards",color:"gold",bold:true}],actions:[{label:{translate:"mgs.multiplayer_level_2",fallback:"Multiplayer Level",color:"gold"},action:{type:"run_command",command:"/trigger mgs.player.config set 1631"}},{label:{translate:"mgs.zombies_level_2",fallback:"Zombies Level",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 1632"}},{label:{translate:"mgs.zombies_maps",fallback:"Zombies Maps",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set 1633"}},{label:{translate:"mgs.missions_maps",fallback:"Missions Maps",color:"aqua"},action:{type:"run_command",command:"/trigger mgs.player.config set 1634"}},{label:{translate:"mgs.settings",fallback:"Settings",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set 1"}}],columns:2,after_action:"close",exit_action:{label:{translate:"gui.done"}}}
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

