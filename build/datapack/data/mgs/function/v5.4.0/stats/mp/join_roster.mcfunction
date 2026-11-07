
#> mgs:v5.4.0/stats/mp/join_roster
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/mp/second
#

scoreboard players operation @s mgs.st.mp.game_id = #st_mp_game mgs.data
data modify storage mgs:stats rosters.mp append from entity @s UUID

