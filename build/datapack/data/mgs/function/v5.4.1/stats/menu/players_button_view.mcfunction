
#> mgs:v5.4.1/stats/menu/players_button_view
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/menu/players_name with storage mgs:temp _sp
#
# @args		name (unknown)
#			trigger (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger)"}}

