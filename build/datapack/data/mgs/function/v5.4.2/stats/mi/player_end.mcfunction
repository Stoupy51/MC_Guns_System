
#> mgs:v5.4.2/stats/mi/player_end
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/snapshot/roster_next with storage mgs:temp _st_one
#

function mgs:v5.4.2/stats/board/levels with storage mgs:temp _st_one
execute if score #st_mi_won mgs.data matches 1 run function mgs:v5.4.2/stats/board/mi_time with storage mgs:temp _st_one

