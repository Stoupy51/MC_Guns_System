
#> mgs:v5.3.0/stats/zb/second
#
# @executed	as @a
#
# @within	mgs:v5.3.0/progression/tick_player
#

scoreboard players add @s mgs.st.zb.time 1
execute unless score @s mgs.st.zb.game_id = #st_zb_game mgs.data run function mgs:v5.3.0/stats/zb/join_roster

