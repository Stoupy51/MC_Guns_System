
#> mgs:v5.4.3/progression/recompute_all
#
# @within	mgs:v5.4.3/dialog/close_then
#

execute as @a run function mgs:v5.4.3/progression/mp/recompute
execute as @a run function mgs:v5.4.3/progression/zb/recompute

scoreboard players reset @a mgs.adv.caught

