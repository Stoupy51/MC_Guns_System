
#> mgs:v5.3.0/stats/menu/players_button_view
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_name with storage mgs:temp _sp
#
# @args		name (unknown)
#			trigger (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger)"}}

