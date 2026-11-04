
#> mgs:v5.3.0/stats/menu/players_button_reset
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/stats/menu/players_name with storage mgs:temp _sp
#
# @args		name (unknown)
#			i (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"yellow"},action:{type:"run_command",command:"/function mgs:v5.3.0/stats/admin/reset {i:$(i)}"}}

