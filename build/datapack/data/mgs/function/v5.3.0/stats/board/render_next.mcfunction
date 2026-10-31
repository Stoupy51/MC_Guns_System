
#> mgs:v5.3.0/stats/board/render_next
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/render {kind:"$(kind)"}
#			mgs:v5.3.0/stats/board/render_next {kind:"$(kind)"}
#
# @args		kind (string)
#

execute unless data storage mgs:temp _lb_walk[0] run return 0
execute if score #lb_k mgs.data matches 10.. run return 0

scoreboard players add #lb_k mgs.data 1
data modify storage mgs:temp _lb_row set from storage mgs:temp _lb_walk[0]
execute store result storage mgs:temp _lb_row.rank int 1 run scoreboard players get #lb_k mgs.data
execute store result score #lb_v mgs.data run data get storage mgs:temp _lb_row.value 0.05
execute store result storage mgs:temp _lb_row.min int 1 run scoreboard players operation #lb_v mgs.data /= #60 mgs.data
execute store result score #lb_v mgs.data run data get storage mgs:temp _lb_row.value 0.05
execute store result score #lb_s mgs.data run scoreboard players operation #lb_v mgs.data %= #60 mgs.data
data modify storage mgs:temp _lb_row.pad set value ""
execute if score #lb_s mgs.data matches ..9 run data modify storage mgs:temp _lb_row.pad set value "0"
execute store result storage mgs:temp _lb_row.sec int 1 run scoreboard players get #lb_s mgs.data
function mgs:v5.3.0/stats/board/row_player with storage mgs:temp _lb_row
$function mgs:v5.3.0/stats/board/row_$(kind) with storage mgs:temp _lb_row

data remove storage mgs:temp _lb_walk[0]
$function mgs:v5.3.0/stats/board/render_next {kind:"$(kind)"}

