
#> mgs:v5.4.2/progression/recompute_all
#
# @within	mgs:v5.4.2/dialog/close_then
#

execute as @a run function mgs:v5.4.2/progression/mp/recompute
execute as @a run function mgs:v5.4.2/progression/zb/recompute

scoreboard players reset @a mgs.adv.caught

