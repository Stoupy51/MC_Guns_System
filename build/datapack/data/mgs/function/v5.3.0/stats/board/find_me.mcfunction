
#> mgs:v5.3.0/stats/board/find_me
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/show
#			mgs:v5.3.0/stats/board/find_me
#

execute unless data storage mgs:temp _lb_walk[0] run return fail
data modify storage mgs:temp _lb_cmp set from storage mgs:temp _lb_walk[0].uuid
execute store success score #lb_diff mgs.data run data modify storage mgs:temp _lb_cmp set from storage mgs:temp _lb_me
execute if score #lb_diff mgs.data matches 0 run return 1
scoreboard players add #lb_k mgs.data 1
data remove storage mgs:temp _lb_walk[0]
return run function mgs:v5.3.0/stats/board/find_me

