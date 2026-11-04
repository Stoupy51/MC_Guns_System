
#> mgs:v5.3.0/stats/mi/join_roster
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/stats/mi/second
#

scoreboard players operation @s mgs.st.mi.game_id = #st_mi_game mgs.data
data modify storage mgs:stats rosters.mi append from entity @s UUID

