
#> mgs:v5.4.2/zombies/xp/on_game_over
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_over
#

scoreboard players operation #xp_gain mgs.data = #final_round mgs.data
scoreboard players operation #xp_gain mgs.data *= #5 mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.4.2/progression/zb/award_game_over

