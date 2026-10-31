
#> mgs:v5.3.0/stats/mp/second
#
# @executed	as @a
#
# @within	mgs:v5.3.0/progression/tick_player
#

scoreboard players add @s mgs.st.mp.time 1
execute unless score @s mgs.st.mp.game_id = #st_mp_game mgs.data run function mgs:v5.3.0/stats/mp/join_roster

