
#> mgs:v5.4.2/stats/board/row_level_zb
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/board/render_next with storage mgs:temp _lb_row
#
# @args		rank (unknown)
#			name (unknown)
#			lzb (unknown)
#

$data modify storage mgs:temp _lb_lines append value ["",{text:"#$(rank) ",color:"gold"},{text:"$(name)",color:"yellow"},{text:" - Level $(lzb)",color:"aqua"},"\n"]

