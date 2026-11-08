
#> mgs:v5.4.1/progression/recompute_all
#
# @within	mgs:v5.4.1/dialog/close_then
#

execute as @a run function mgs:v5.4.1/progression/mp/recompute
execute as @a run function mgs:v5.4.1/progression/zb/recompute

scoreboard players reset @a mgs.adv.caught

