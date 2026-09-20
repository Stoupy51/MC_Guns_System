
#> mgs:v5.1.0/progression/zb/level_check
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/progression/zb/settle
#			mgs:v5.1.0/progression/zb/level_up
#

scoreboard players operation #xp_req mgs.data = @s mgs.zb.xp_level
scoreboard players operation #xp_req mgs.data *= #10 mgs.data
scoreboard players add #xp_req mgs.data 40
execute if score @s mgs.zb.xp_prog >= #xp_req mgs.data run function mgs:v5.1.0/progression/zb/level_up

