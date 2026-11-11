
#> mgs:v5.4.2/progression/mp/level_up
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/progression/mp/level_check
#

scoreboard players operation @s mgs.mp.xp_prog -= #xp_req mgs.data
scoreboard players add @s mgs.mp.xp_level 1
function mgs:v5.4.2/progression/mp/level_check

