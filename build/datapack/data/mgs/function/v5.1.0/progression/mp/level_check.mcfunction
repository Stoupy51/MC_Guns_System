
#> mgs:v5.1.0/progression/mp/level_check
#
# @within	mgs:v5.1.0/progression/mp/settle
#			mgs:v5.1.0/progression/mp/level_up
#

scoreboard players operation #xp_req mgs.data = @s mgs.mp.xp_level
scoreboard players operation #xp_req mgs.data *= #10 mgs.data
scoreboard players add #xp_req mgs.data 40
execute if score @s mgs.mp.xp_prog >= #xp_req mgs.data run function mgs:v5.1.0/progression/mp/level_up

