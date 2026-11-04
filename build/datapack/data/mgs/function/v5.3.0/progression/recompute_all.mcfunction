
#> mgs:v5.3.0/progression/recompute_all
#
# @within	mgs:v5.3.0/dialog/close_then
#

execute as @a run function mgs:v5.3.0/progression/mp/recompute
execute as @a run function mgs:v5.3.0/progression/zb/recompute

scoreboard players reset @a mgs.adv.caught

