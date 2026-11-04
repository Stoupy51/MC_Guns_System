
#> mgs:v5.3.0/stats/zb/join_roster
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/stats/zb/second
#

scoreboard players operation @s mgs.st.zb.game_id = #st_zb_game mgs.data
data modify storage mgs:stats rosters.zb append from entity @s UUID

