
#> mgs:v5.4.4/stats/board/forget_mi_next
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/board/forget
#			mgs:v5.4.4/stats/board/forget_mi_next
#

execute unless data storage mgs:temp _fg.maps[0] run return 0
data modify storage mgs:temp _fg.id set from storage mgs:temp _fg.maps[0].id
function mgs:v5.4.4/stats/board/forget_mi_one with storage mgs:temp _fg
data remove storage mgs:temp _fg.maps[0]
function mgs:v5.4.4/stats/board/forget_mi_next

