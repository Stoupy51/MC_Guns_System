
#> mgs:v5.4.2/stats/board/row_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/board/render_next with storage mgs:temp _lb_row
#
# @args		uuid (unknown)
#

$data modify storage mgs:temp _lb_row.name set from storage mgs:stats players."$(uuid)".name
$data modify storage mgs:temp _lb_row.level set from storage mgs:stats players."$(uuid)".level
data modify storage mgs:temp _lb_row.lmp set from storage mgs:temp _lb_row.level.mp
data modify storage mgs:temp _lb_row.lzb set from storage mgs:temp _lb_row.level.zb

