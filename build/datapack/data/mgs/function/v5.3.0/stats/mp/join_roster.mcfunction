
#> mgs:v5.3.0/stats/mp/join_roster
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/mp/second
#

scoreboard players operation @s mgs.st.mp.game_id = #st_mp_game mgs.data
data modify storage mgs:stats rosters.mp append from entity @s UUID

