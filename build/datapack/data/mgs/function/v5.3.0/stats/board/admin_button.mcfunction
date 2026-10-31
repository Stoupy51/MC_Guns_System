
#> mgs:v5.3.0/stats/board/admin_button
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/stats/board/admin_next with storage mgs:temp _lb_maps[0]
#
# @args		label (unknown)
#			name (unknown)
#			board (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(label): $(name)",color:"yellow"},action:{type:"run_command",command:"/function mgs:v5.3.0/stats/admin/reset_board {board:$(board),id:$(id)}"}}

