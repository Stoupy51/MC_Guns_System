
#> mgs:v5.3.0/stats/board/walk
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/board/insert
#			mgs:v5.3.0/stats/board/walk
#

execute unless data storage mgs:temp _lb_walk[0] run return 0
execute store result score #lb_v mgs.data run data get storage mgs:temp _lb_walk[0].value
execute if score #lb_desc mgs.data matches 1 if score #lb_v mgs.data < #lb_new mgs.data run return 0
execute if score #lb_desc mgs.data matches 0 if score #lb_v mgs.data > #lb_new mgs.data run return 0
scoreboard players add #lb_k mgs.data 1
data remove storage mgs:temp _lb_walk[0]
function mgs:v5.3.0/stats/board/walk

