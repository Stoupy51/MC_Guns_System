
#> mgs:v5.3.0/stats/board/row_mi_map
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/stats/board/render_next with storage mgs:temp _lb_row
#
# @args		rank (unknown)
#			name (unknown)
#			min (unknown)
#			pad (unknown)
#			sec (unknown)
#			players (unknown)
#

$data modify storage mgs:temp _lb_lines append value ["",{text:"#$(rank) ",color:"gold"},{text:"$(name)",color:"yellow"},{text:" - $(min):$(pad)$(sec)",color:"aqua"},{text:" ($(players)P)",color:"gray"},"\n"]

