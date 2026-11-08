
#> mgs:v5.4.1/stats/zb/second
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/progression/tick_player
#

scoreboard players add @s mgs.st.zb.time 1
execute unless score @s mgs.st.zb.game_id = #st_zb_game mgs.data run function mgs:v5.4.1/stats/zb/join_roster

