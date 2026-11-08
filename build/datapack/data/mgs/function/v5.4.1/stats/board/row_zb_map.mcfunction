
#> mgs:v5.4.1/stats/board/row_zb_map
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/board/render_next with storage mgs:temp _lb_row
#
# @args		players (int)
#			rank (unknown)
#			name (unknown)
#			value (unknown)
#

$data modify storage mgs:temp _lb_lines append value ["",{text:"#$(rank) ",color:"gold"},{text:"$(name)",color:"yellow"},{text:" - Round $(value)",color:"red"},{text:" ($(players)P)",color:"gray"},"\n"]

