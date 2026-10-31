
#> mgs:v5.3.0/stats/mi/second
#
# @executed	as @a
#
# @within	mgs:v5.3.0/progression/tick_player
#

scoreboard players add @s mgs.st.mi.time 1
execute unless score @s mgs.st.mi.game_id = #st_mi_game mgs.data run function mgs:v5.3.0/stats/mi/join_roster

