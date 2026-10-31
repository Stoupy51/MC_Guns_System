
#> mgs:v5.3.0/stats/zb/join_roster
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/zb/second
#

scoreboard players operation @s mgs.st.zb.game_id = #st_zb_game mgs.data
data modify storage mgs:stats rosters.zb append from entity @s UUID

