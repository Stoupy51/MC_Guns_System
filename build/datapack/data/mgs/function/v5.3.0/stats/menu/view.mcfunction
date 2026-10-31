
#> mgs:v5.3.0/stats/menu/view
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/mine
#			mgs:v5.3.0/stats/menu/view_trigger
#

data modify storage mgs:temp _sv set value {}
execute store result storage mgs:temp _sv.i int 1 run scoreboard players get #st_i mgs.data
function mgs:v5.3.0/stats/menu/fetch with storage mgs:temp _sv
execute unless data storage mgs:temp _sv.p run return fail

execute if score #st_m mgs.data matches 0 run function mgs:v5.3.0/stats/menu/zb
execute if score #st_m mgs.data matches 1 run function mgs:v5.3.0/stats/menu/mp
execute if score #st_m mgs.data matches 2 run function mgs:v5.3.0/stats/menu/mi

