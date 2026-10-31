
#> mgs:v5.3.0/stats/mi/join_roster
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/mi/second
#

scoreboard players operation @s mgs.st.mi.game_id = #st_mi_game mgs.data
data modify storage mgs:stats rosters.mi append from entity @s UUID

