
#> mgs:v5.4.2/stats/mi/join_roster
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/mi/second
#

scoreboard players operation @s mgs.st.mi.game_id = #st_mi_game mgs.data
data modify storage mgs:stats rosters.mi append from entity @s UUID

