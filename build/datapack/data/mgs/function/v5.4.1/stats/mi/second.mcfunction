
#> mgs:v5.4.1/stats/mi/second
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/progression/tick_player
#

scoreboard players add @s mgs.st.mi.time 1
execute unless score @s mgs.st.mi.game_id = #st_mi_game mgs.data run function mgs:v5.4.1/stats/mi/join_roster

