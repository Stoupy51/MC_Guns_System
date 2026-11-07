
#> mgs:v5.4.0/progression/zb/level_up
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/progression/zb/level_check
#

scoreboard players operation @s mgs.zb.xp_prog -= #xp_req mgs.data
scoreboard players add @s mgs.zb.xp_level 1
function mgs:v5.4.0/progression/zb/level_check

