
#> mgs:v5.3.0/stats/board/row_player
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/render_next with storage mgs:temp _lb_row
#
# @args		uuid (unknown)
#

$data modify storage mgs:temp _lb_row.name set from storage mgs:stats players."$(uuid)".name
$data modify storage mgs:temp _lb_row.level set from storage mgs:stats players."$(uuid)".level
data modify storage mgs:temp _lb_row.lmp set from storage mgs:temp _lb_row.level.mp
data modify storage mgs:temp _lb_row.lzb set from storage mgs:temp _lb_row.level.zb

