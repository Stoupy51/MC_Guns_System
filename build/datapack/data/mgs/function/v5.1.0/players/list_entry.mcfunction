
#> mgs:v5.1.0/players/list_entry
#
# @within	mgs:v5.1.0/players/list_iter with storage mgs:temp _plr_entry
#
# @args		name (unknown)
#			color (unknown)
#			mode (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.click_to_manage_this_player"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/$(mode)_menu {id:$(id),name:\"$(name)\"}"}}

