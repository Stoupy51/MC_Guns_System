
#> mgs:v5.4.1/progression/zb/level_check
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/progression/zb/settle
#			mgs:v5.4.1/progression/zb/level_up
#

scoreboard players operation #xp_req mgs.data = @s mgs.zb.xp_level
scoreboard players operation #xp_req mgs.data *= #10 mgs.data
scoreboard players add #xp_req mgs.data 40
execute if score @s mgs.zb.xp_prog >= #xp_req mgs.data run function mgs:v5.4.1/progression/zb/level_up

