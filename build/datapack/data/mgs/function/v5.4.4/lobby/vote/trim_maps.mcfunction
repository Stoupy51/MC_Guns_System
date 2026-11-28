
#> mgs:v5.4.4/lobby/vote/trim_maps
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/collect_maps
#			mgs:v5.4.4/lobby/vote/trim_maps
#

execute store result score #lv_n mgs.data if data storage mgs:temp _lv_opts[]
execute if score #lv_n mgs.data matches ..7 run return 0
scoreboard players remove #lv_n mgs.data 1
execute store result storage mgs:temp _lv_pick.max int 1 run scoreboard players get #lv_n mgs.data
function mgs:v5.4.4/lobby/vote/drop_random with storage mgs:temp _lv_pick
function mgs:v5.4.4/lobby/vote/trim_maps

