
#> mgs:v5.3.0/stats/menu/zb_tabs
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/zb_dialog with storage mgs:temp _sv.t
#
# @args		trigger_zb (unknown)
#			trigger_mp (unknown)
#			trigger_mi (unknown)
#

$data modify storage mgs:temp dialog.actions set value [{label:{translate:"mgs.zombies",fallback:"Zombies",color:"gold"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger_zb)"}},{label:{translate:"mgs.multiplayer",fallback:"Multiplayer",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger_mp)"}},{label:{translate:"mgs.missions",fallback:"Missions",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger_mi)"}}]
data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.players_2",fallback:"Players",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set 90000"}}
data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.settings",fallback:"Settings",color:"aqua"},action:{type:"run_command",command:"/trigger mgs.player.config set 1"}}

